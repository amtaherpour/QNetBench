"""Strict SweepSpec v0.1 loading and deterministic finite expansion."""

from __future__ import annotations

import hashlib
import json
import math
import re
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Annotated, Any, Literal, NoReturn

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StrictBool,
    StrictInt,
    StrictStr,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)

from qnetbench.errors import ConfigError, SweepError
from qnetbench.spec import BenchmarkSpec, benchmark_hash, load_benchmark

_SWEEP_ID_PATTERN = r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
_APPROVED_EXACT_PATHS = {
    "physical_profile.memory_count_per_node",
    "physical_profile.memory_coherence_time_s",
    "physical_profile.memory_frequency_hz",
    "physical_profile.memory_efficiency",
    "physical_profile.detector_efficiency",
    "physical_profile.fiber_attenuation_db_per_km",
    "physical_profile.quantum_propagation_speed_km_per_s",
    "physical_profile.classical_propagation_speed_km_per_s",
    "physical_profile.link_fidelity",
    "physical_profile.swap_success_probability",
    "physical_profile.swap_fidelity_factor",
    "workload.request_count",
    "workload.batch_start_s",
    "workload.deadline_s",
}
_LINK_LENGTH_PATH = re.compile(r"^network\.links\.(0|[1-9][0-9]*)\.length_km$")

type SweepScalar = StrictBool | StrictInt | FiniteFloat | StrictStr


class _StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        validate_default=True,
    )


class SweepAxis(_StrictModel):
    """One approved scalar benchmark field and its finite source-ordered values."""

    path: Annotated[StrictStr, StringConstraints(min_length=1)]
    values: tuple[SweepScalar, ...] = Field(min_length=1)

    @field_validator("values", mode="before")
    @classmethod
    def normalize_values(cls, value: object) -> object:
        return tuple(value) if isinstance(value, list) else value

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        if value not in _APPROVED_EXACT_PATHS and not _LINK_LENGTH_PATH.fullmatch(
            value
        ):
            raise ValueError("path is not an approved alpha scalar replacement")
        return value

    @model_validator(mode="after")
    def validate_unique_finite_values(self) -> SweepAxis:
        markers: list[tuple[str, str]] = []
        for value in self.values:
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("axis values must be finite")
            marker = (type(value).__name__, repr(value))
            if marker in markers:
                raise ValueError("axis values must be unique")
            markers.append(marker)
        return self


class SweepSpec(_StrictModel):
    """Versioned, backend-independent finite sweep description."""

    sweep_schema_version: Literal["0.1"]
    sweep_id: Annotated[StrictStr, StringConstraints(pattern=_SWEEP_ID_PATTERN)]
    base_benchmark: Annotated[StrictStr, StringConstraints(min_length=1)]
    output_root: Annotated[StrictStr, StringConstraints(min_length=1)]
    axes: tuple[SweepAxis, ...] = Field(min_length=1)
    seeds: tuple[StrictInt, ...] = Field(min_length=1)

    @field_validator("axes", "seeds", mode="before")
    @classmethod
    def normalize_sequences(cls, value: object) -> object:
        return tuple(value) if isinstance(value, list) else value

    @field_validator("output_root")
    @classmethod
    def validate_output_root(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("output_root must be a safe relative path")
        return value

    @model_validator(mode="after")
    def validate_unique_axes_and_seeds(self) -> SweepSpec:
        paths = [axis.path for axis in self.axes]
        if len(paths) != len(set(paths)):
            raise ValueError("axis paths must be unique")
        if len(self.seeds) != len(set(self.seeds)):
            raise ValueError("seeds must be unique")
        return self


@dataclass(frozen=True)
class LoadedSweep:
    """A validated sweep plus the source path used for relative resolution."""

    source: Path
    spec: SweepSpec

    @property
    def base_benchmark_path(self) -> Path:
        return (self.source.parent / self.spec.base_benchmark).resolve()

    @property
    def default_output_path(self) -> Path:
        return (self.source.parent / self.spec.output_root).resolve()


@dataclass(frozen=True)
class ExpandedCase:
    """One deterministic benchmark/seed combination before backend planning."""

    index: int
    parameters: tuple[tuple[str, SweepScalar], ...]
    seed: int
    benchmark: BenchmarkSpec
    benchmark_hash: str

    @property
    def parameter_map(self) -> dict[str, SweepScalar]:
        return dict(self.parameters)


def _reject_json_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON constant {value!r} is not allowed")


def _format_validation_error(error: ValidationError) -> str:
    details: list[str] = []
    for item in error.errors(include_url=False):
        location = ".".join(str(part) for part in item["loc"]) or "sweep"
        details.append(f"{location}: {item['msg']}")
    return "invalid SweepSpec v0.1: " + "; ".join(details)


def load_sweep(source: str | Path) -> LoadedSweep:
    """Safely load one YAML/JSON SweepSpec or raise a path-aware error."""
    path = Path(source)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ConfigError(f"could not read sweep: {error}", source=path) from error
    try:
        if path.suffix.lower() == ".json":
            document = json.loads(text, parse_constant=_reject_json_constant)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            document = yaml.safe_load(text)
        else:
            raise ConfigError(
                "unsupported sweep format; expected .yaml, .yml, or .json",
                source=path,
            )
    except ConfigError:
        raise
    except (json.JSONDecodeError, ValueError, yaml.YAMLError) as error:
        raise ConfigError(f"could not parse sweep: {error}", source=path) from error
    if not isinstance(document, dict):
        raise ConfigError("sweep document must be a mapping", source=path)
    try:
        spec = SweepSpec.model_validate(document)
    except ValidationError as error:
        raise ConfigError(_format_validation_error(error), source=path) from error
    return LoadedSweep(source=path.resolve(), spec=spec)


def canonical_sweep_json(spec: SweepSpec) -> str:
    """Return deterministic JSON for SweepSpec identity and audit records."""
    return json.dumps(
        spec.model_dump(mode="json"),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sweep_hash(spec: SweepSpec) -> str:
    return hashlib.sha256(canonical_sweep_json(spec).encode("utf-8")).hexdigest()


def _set_scalar(document: dict[str, Any], path: str, value: SweepScalar) -> None:
    parts = path.split(".")
    target: Any = document
    for part in parts[:-1]:
        if isinstance(target, list):
            try:
                target = target[int(part)]
            except (ValueError, IndexError) as error:
                raise SweepError(f"invalid sweep path {path!r}") from error
        elif isinstance(target, dict) and part in target:
            target = target[part]
        else:
            raise SweepError(f"invalid sweep path {path!r}")
    leaf = parts[-1]
    if isinstance(target, list):
        try:
            index = int(leaf)
            current = target[index]
        except (ValueError, IndexError) as error:
            raise SweepError(f"invalid sweep path {path!r}") from error
        if isinstance(current, (dict, list)):
            raise SweepError(f"sweep path {path!r} is not scalar")
        target[index] = value
    elif isinstance(target, dict) and leaf in target:
        if isinstance(target[leaf], (dict, list)):
            raise SweepError(f"sweep path {path!r} is not scalar")
        target[leaf] = value
    else:
        raise SweepError(f"invalid sweep path {path!r}")


def expand_sweep(loaded: LoadedSweep, *, cap: int = 100) -> tuple[ExpandedCase, ...]:
    """Expand axes lexically, values in source order, then seeds in source order."""
    if cap < 1:
        raise ValueError("cap must be positive")
    base = load_benchmark(loaded.base_benchmark_path)
    axes = tuple(sorted(loaded.spec.axes, key=lambda axis: axis.path))
    run_count = math.prod(len(axis.values) for axis in axes) * len(loaded.spec.seeds)
    if run_count > cap:
        raise SweepError(
            f"sweep expands to {run_count} runs, exceeding the alpha cap of {cap}"
        )
    cases: list[ExpandedCase] = []
    index = 0
    for values in product(*(axis.values for axis in axes)):
        parameters = tuple((axis.path, value) for axis, value in zip(axes, values))
        for seed in loaded.spec.seeds:
            index += 1
            data = deepcopy(base.model_dump(mode="json"))
            for path, value in parameters:
                _set_scalar(data, path, value)
            try:
                resolved = BenchmarkSpec.model_validate(data)
            except ValidationError as error:
                details = _format_validation_error(error).replace(
                    "SweepSpec", "resolved BenchmarkSpec"
                )
                raise SweepError(
                    f"expanded case {index} is invalid after replacements: {details}"
                ) from error
            cases.append(
                ExpandedCase(
                    index=index,
                    parameters=parameters,
                    seed=int(seed),
                    benchmark=resolved,
                    benchmark_hash=benchmark_hash(resolved),
                )
            )
    return tuple(cases)
