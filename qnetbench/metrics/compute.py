"""Pure v0.1 metric calculations over canonical manifest and request records."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from statistics import fmean, median

from qnetbench.errors import MetricComputationError
from qnetbench.metrics.definitions import METRIC_DEFINITIONS, METRIC_IDS
from qnetbench.results import MetricRow, RequestResult, RunManifest


def _row(
    metric_id: str,
    *,
    status: str,
    value: float | None,
    population: int,
    coverage: int,
) -> MetricRow:
    return MetricRow(
        metric_id=metric_id,
        status=status,
        value=value,
        unit=METRIC_DEFINITIONS[metric_id].unit,
        population_count=population,
        coverage_count=coverage,
    )


def _validate_inputs(manifest: RunManifest, requests: Sequence[RequestResult]) -> None:
    if manifest.status != "complete":
        raise MetricComputationError("metrics require a complete run manifest")
    if len(requests) != manifest.expected_request_count:
        raise MetricComputationError(
            "request record count must equal manifest.expected_request_count"
        )
    if manifest.expected_request_count <= 0:
        raise MetricComputationError("planned request count must be positive")
    if manifest.written_request_count != len(requests):
        raise MetricComputationError(
            "request record count must equal manifest.written_request_count"
        )
    identifiers = [record.request_id for record in requests]
    if len(identifiers) != len(set(identifiers)):
        raise MetricComputationError("request IDs must be unique")


def _nearest_rank_p95(values: Sequence[float]) -> float:
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def compute_metrics(
    manifest: RunManifest,
    requests: Sequence[RequestResult],
    metric_ids: Iterable[str] = METRIC_IDS,
) -> tuple[MetricRow, ...]:
    """Compute requested standard metrics in caller-supplied order."""
    _validate_inputs(manifest, requests)
    requested = tuple(metric_ids)
    unknown = [
        metric_id for metric_id in requested if metric_id not in METRIC_DEFINITIONS
    ]
    if unknown:
        raise MetricComputationError(f"unknown metric ID {unknown[0]!r}")
    if len(requested) != len(set(requested)):
        raise MetricComputationError("metric_ids contains a duplicate metric ID")

    successes = tuple(record for record in requests if record.status == "success")
    success_count = len(successes)
    planned_count = manifest.expected_request_count
    latency_values = tuple(record.latency_s for record in successes)
    fidelity_values = tuple(
        record.fidelity for record in successes if record.fidelity is not None
    )
    attempts_values = tuple(
        record.attempts for record in requests if record.attempts is not None
    )

    rows: dict[str, MetricRow] = {}
    rows["request_success_probability"] = _row(
        "request_success_probability",
        status="ok",
        value=success_count / planned_count,
        population=planned_count,
        coverage=len(requests),
    )

    latency_status = "ok" if success_count else "unavailable"
    latency_functions = {
        "latency_mean_s": lambda: fmean(latency_values),
        "latency_median_s": lambda: median(latency_values),
        "latency_p95_s": lambda: _nearest_rank_p95(latency_values),
    }
    for metric_id, function in latency_functions.items():
        rows[metric_id] = _row(
            metric_id,
            status=latency_status,
            value=float(function()) if success_count else None,
            population=success_count,
            coverage=success_count,
        )

    fidelity_complete = success_count > 0 and len(fidelity_values) == success_count
    fidelity_status = "ok" if fidelity_complete else "unavailable"
    rows["fidelity_mean"] = _row(
        "fidelity_mean",
        status=fidelity_status,
        value=float(fmean(fidelity_values)) if fidelity_complete else None,
        population=success_count,
        coverage=len(fidelity_values),
    )
    rows["fidelity_median"] = _row(
        "fidelity_median",
        status=fidelity_status,
        value=float(median(fidelity_values)) if fidelity_complete else None,
        population=success_count,
        coverage=len(fidelity_values),
    )

    duration = manifest.measurement_end_s - manifest.measurement_start_s
    throughput_ok = duration > 0
    rows["throughput_success_per_s"] = _row(
        "throughput_success_per_s",
        status="ok" if throughput_ok else "unavailable",
        value=success_count / duration if throughput_ok else None,
        population=success_count,
        coverage=success_count,
    )

    attempts_complete = len(attempts_values) == planned_count
    attempts_ok = attempts_complete and success_count > 0
    rows["attempts_per_success"] = _row(
        "attempts_per_success",
        status="ok" if attempts_ok else "unavailable",
        value=sum(attempts_values) / success_count if attempts_ok else None,
        population=planned_count,
        coverage=len(attempts_values),
    )
    return tuple(rows[metric_id] for metric_id in requested)
