"""Canonical result models for contract version 0.1."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StringConstraints,
    field_validator,
    model_validator,
)

_IDENTIFIER_PATTERN = r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
_HASH_PATTERN = r"^[0-9a-f]{64}$"
Identifier = Annotated[str, StringConstraints(pattern=_IDENTIFIER_PATTERN)]
HashValue = Annotated[str, StringConstraints(pattern=_HASH_PATTERN)]
NonEmptyString = Annotated[str, StringConstraints(min_length=1)]
NonNegativeFloat = Annotated[FiniteFloat, Field(ge=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
Probability = Annotated[FiniteFloat, Field(ge=0, le=1)]

RunStatus = Literal["complete", "failed"]
RequestStatus = Literal["success", "failed", "timed_out", "rejected"]
MetricStatus = Literal["ok", "unavailable", "not_applicable"]
MetricId = Literal[
    "request_success_probability",
    "latency_mean_s",
    "latency_median_s",
    "latency_p95_s",
    "fidelity_mean",
    "fidelity_median",
    "throughput_success_per_s",
    "attempts_per_success",
]
ErrorStage = Literal[
    "validation",
    "support_check",
    "execution",
    "normalization",
    "metrics",
    "artifact_write",
]


class StrictResultModel(BaseModel):
    """Shared strict, immutable model configuration."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        validate_default=True,
    )


class RunManifest(StrictResultModel):
    """Identity, provenance, timing, and count data for one run."""

    result_schema_version: Literal["0.1"]
    run_id: NonEmptyString
    benchmark_id: Identifier
    benchmark_hash: HashValue
    execution_hash: HashValue
    qnetbench_version: NonEmptyString
    adapter_name: NonEmptyString
    adapter_version: NonEmptyString
    backend_name: NonEmptyString
    backend_version: str | None
    seed: int
    status: RunStatus
    started_at_utc: NonEmptyString
    ended_at_utc: NonEmptyString
    measurement_start_s: FiniteFloat
    measurement_end_s: FiniteFloat
    expected_request_count: NonNegativeInt
    written_request_count: NonNegativeInt
    python_version: NonEmptyString
    platform: NonEmptyString
    warnings: tuple[str, ...]
    support_report_digest: NonEmptyString

    @field_validator("warnings", mode="before")
    @classmethod
    def normalize_warnings(cls, value: object) -> object:
        """Accept the JSON array encoding and store warnings immutably."""
        return tuple(value) if isinstance(value, list) else value

    @staticmethod
    def _parse_utc(value: str, field_name: str) -> datetime:
        if not value.endswith("Z"):
            raise ValueError(f"{field_name} must use a UTC 'Z' suffix")
        try:
            return datetime.fromisoformat(value[:-1] + "+00:00")
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be an ISO-8601 UTC timestamp"
            ) from error

    @model_validator(mode="after")
    def validate_relations(self) -> RunManifest:
        """Validate timestamp, measurement-window, and count relations."""
        started = self._parse_utc(self.started_at_utc, "started_at_utc")
        ended = self._parse_utc(self.ended_at_utc, "ended_at_utc")
        if ended < started:
            raise ValueError("ended_at_utc must not precede started_at_utc")
        if self.measurement_end_s < self.measurement_start_s:
            raise ValueError("measurement_end_s must not precede measurement_start_s")
        if self.written_request_count > self.expected_request_count:
            raise ValueError(
                "written_request_count must not exceed expected_request_count"
            )
        if self.status == "complete" and (
            self.written_request_count != self.expected_request_count
        ):
            raise ValueError(
                "a complete manifest requires written_request_count to equal "
                "expected_request_count"
            )
        return self


class RequestResult(StrictResultModel):
    """One terminal canonical outcome for one planned request."""

    request_id: NonEmptyString
    source: Identifier
    destination: Identifier
    submitted_at_s: NonNegativeFloat
    terminal_at_s: NonNegativeFloat
    status: RequestStatus
    latency_s: NonNegativeFloat
    fidelity: Probability | None
    attempts: NonNegativeInt | None
    path: tuple[Identifier, ...] | None
    failure_reason: str | None
    metadata: dict[str, Any]

    @field_validator("path", mode="before")
    @classmethod
    def normalize_path(cls, value: object) -> object:
        """Accept the JSON array encoding and store paths immutably."""
        return tuple(value) if isinstance(value, list) else value

    @field_validator("path")
    @classmethod
    def validate_path_length(
        cls, value: tuple[Identifier, ...] | None
    ) -> tuple[Identifier, ...] | None:
        if value is not None and len(value) < 2:
            raise ValueError("path must contain at least two nodes")
        return value

    @staticmethod
    def _validate_metadata(value: object, location: str = "metadata") -> None:
        if value is None or isinstance(value, (str, bool, int)):
            return
        if isinstance(value, float):
            if not math.isfinite(value):
                raise ValueError(f"{location} contains a non-finite number")
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                RequestResult._validate_metadata(item, f"{location}[{index}]")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                if not isinstance(key, str):
                    raise ValueError(f"{location} contains a non-string key")
                RequestResult._validate_metadata(item, f"{location}.{key}")
            return
        raise ValueError(f"{location} contains a non-JSON value")

    @model_validator(mode="after")
    def validate_terminal_record(self) -> RequestResult:
        """Enforce terminal timing and status-dependent invariants."""
        if self.source == self.destination:
            raise ValueError("destination must differ from source")
        if self.terminal_at_s < self.submitted_at_s:
            raise ValueError("terminal_at_s must not precede submitted_at_s")
        expected_latency = self.terminal_at_s - self.submitted_at_s
        if not math.isclose(
            self.latency_s,
            expected_latency,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            raise ValueError("latency_s must equal terminal_at_s - submitted_at_s")
        if self.status == "success":
            if self.failure_reason is not None:
                raise ValueError("successful requests must not have failure_reason")
        elif self.fidelity is not None:
            raise ValueError("non-success requests must have fidelity=null")
        if self.path is not None:
            if self.path[0] != self.source:
                raise ValueError("path[0] must equal source")
            if self.path[-1] != self.destination:
                raise ValueError("path[-1] must equal destination")
        self._validate_metadata(self.metadata)
        return self


class MetricRow(StrictResultModel):
    """One stable metric CSV row."""

    metric_id: MetricId
    status: MetricStatus
    value: FiniteFloat | None
    unit: str | None
    population_count: NonNegativeInt
    coverage_count: NonNegativeInt

    @model_validator(mode="after")
    def validate_availability(self) -> MetricRow:
        """Keep availability state, value, and coverage internally consistent."""
        if self.coverage_count > self.population_count:
            raise ValueError("coverage_count must not exceed population_count")
        if self.status == "ok" and self.value is None:
            raise ValueError("ok metrics require a value")
        if self.status != "ok" and self.value is not None:
            raise ValueError("non-ok metrics require value=null")
        return self


class Summary(StrictResultModel):
    """Derived convenience summary; never a metric input."""

    result_schema_version: Literal["0.1"]
    run_id: NonEmptyString
    status: RunStatus
    metrics: dict[str, FiniteFloat | None]


class ErrorRecord(StrictResultModel):
    """Sanitized failed-run error record."""

    error_schema_version: Literal["0.1"]
    exception_type: NonEmptyString
    message: NonEmptyString
    stage: ErrorStage
    traceback: str
