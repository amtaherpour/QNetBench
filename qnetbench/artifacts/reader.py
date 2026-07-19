"""Safe readers for canonical QNetBench result bundles."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn

from pydantic import ValidationError

from qnetbench.errors import ArtifactError, ConfigError, ResultValidationError
from qnetbench.results import (
    ErrorRecord,
    MetricRow,
    RequestResult,
    RunManifest,
    Summary,
    validate_bundle,
)
from qnetbench.spec import BenchmarkSpec, load_benchmark

_METRIC_COLUMNS = (
    "metric_id",
    "status",
    "value",
    "unit",
    "population_count",
    "coverage_count",
)


@dataclass(frozen=True)
class RunBundle:
    """One validated canonical result bundle."""

    path: Path
    benchmark: BenchmarkSpec
    manifest: RunManifest
    requests: tuple[RequestResult, ...] = ()
    metrics: tuple[MetricRow, ...] = ()
    summary: Summary | None = None
    error: ErrorRecord | None = None


def _reject_json_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON constant {value!r} is not allowed")


def _read_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text, parse_constant=_reject_json_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ArtifactError(f"{path}: could not read valid JSON: {error}") from error


def _model(path: Path, model_type: type[Any]) -> Any:
    try:
        return model_type.model_validate(_read_json(path))
    except ValidationError as error:
        raise ArtifactError(f"{path}: invalid canonical data: {error}") from error


def _read_requests(path: Path) -> tuple[RequestResult, ...]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ArtifactError(f"{path}: could not read JSONL: {error}") from error
    records: list[RequestResult] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise ArtifactError(f"{path}:{line_number}: blank JSONL line")
        try:
            data = json.loads(line, parse_constant=_reject_json_constant)
            records.append(RequestResult.model_validate(data))
        except (json.JSONDecodeError, ValueError, ValidationError) as error:
            raise ArtifactError(
                f"{path}:{line_number}: invalid request record: {error}"
            ) from error
    return tuple(records)


def _read_metrics(path: Path) -> tuple[MetricRow, ...]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != _METRIC_COLUMNS:
                raise ArtifactError(
                    f"{path}: expected CSV columns {','.join(_METRIC_COLUMNS)}"
                )
            rows: list[MetricRow] = []
            for line_number, row in enumerate(reader, start=2):
                try:
                    data = {
                        "metric_id": row["metric_id"],
                        "status": row["status"],
                        "value": None if row["value"] == "" else float(row["value"]),
                        "unit": None if row["unit"] == "" else row["unit"],
                        "population_count": int(row["population_count"]),
                        "coverage_count": int(row["coverage_count"]),
                    }
                    rows.append(MetricRow.model_validate(data))
                except (KeyError, TypeError, ValueError, ValidationError) as error:
                    raise ArtifactError(
                        f"{path}:{line_number}: invalid metric row: {error}"
                    ) from error
            return tuple(rows)
    except ArtifactError:
        raise
    except (OSError, UnicodeError, csv.Error) as error:
        raise ArtifactError(f"{path}: could not read metrics CSV: {error}") from error


def _require_file(directory: Path, name: str) -> Path:
    path = directory / name
    if not path.is_file():
        raise ArtifactError(f"{path}: required bundle file is missing")
    return path


def read_bundle(source: str | Path) -> RunBundle:
    """Read and validate one complete or failed result bundle."""
    directory = Path(source)
    if not directory.is_dir():
        raise ArtifactError(f"{directory}: bundle directory does not exist")
    try:
        benchmark = load_benchmark(_require_file(directory, "benchmark.yaml"))
    except ConfigError as error:
        raise ArtifactError(str(error)) from error
    manifest = _model(
        _require_file(directory, "run_manifest.json"),
        RunManifest,
    )

    requests: tuple[RequestResult, ...] = ()
    metrics: tuple[MetricRow, ...] = ()
    summary: Summary | None = None
    error: ErrorRecord | None = None

    if manifest.status == "complete":
        if (directory / "error.json").exists():
            raise ArtifactError(
                f"{directory / 'error.json'}: not allowed for complete run"
            )
        requests = _read_requests(_require_file(directory, "requests.jsonl"))
        metrics = _read_metrics(_require_file(directory, "metrics.csv"))
        summary = _model(_require_file(directory, "summary.json"), Summary)
    else:
        if (directory / "metrics.csv").exists() or (
            directory / "summary.json"
        ).exists():
            raise ArtifactError(f"{directory}: failed run contains standard metrics")
        error = _model(_require_file(directory, "error.json"), ErrorRecord)

    try:
        validate_bundle(
            benchmark,
            manifest,
            requests=requests,
            metrics=metrics,
            summary=summary,
            error=error,
        )
    except ResultValidationError as validation_error:
        raise ArtifactError(
            f"{directory}: invalid result bundle: {validation_error}"
        ) from validation_error
    return RunBundle(
        path=directory,
        benchmark=benchmark,
        manifest=manifest,
        requests=requests,
        metrics=metrics,
        summary=summary,
        error=error,
    )
