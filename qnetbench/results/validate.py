"""Cross-record and bundle-level canonical result validation."""

from __future__ import annotations

import math
from collections.abc import Sequence

from qnetbench.errors import ResultValidationError
from qnetbench.results.models import (
    ErrorRecord,
    MetricRow,
    RequestResult,
    RunManifest,
    Summary,
)
from qnetbench.spec import BenchmarkSpec, benchmark_hash


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ResultValidationError(message)


def _validate_manifest_identity(
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
) -> None:
    _require(
        manifest.benchmark_id == benchmark.benchmark_id,
        "run_manifest.benchmark_id does not match benchmark.yaml",
    )
    actual_hash = benchmark_hash(benchmark)
    _require(
        manifest.benchmark_hash == actual_hash,
        "run_manifest.benchmark_hash does not match benchmark.yaml",
    )
    _require(
        manifest.expected_request_count == benchmark.workload.request_count,
        "run_manifest.expected_request_count does not match benchmark workload",
    )


def _validate_requests(
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    requests: Sequence[RequestResult],
) -> None:
    _require(
        manifest.written_request_count == len(requests),
        "run_manifest.written_request_count does not match requests.jsonl",
    )
    positions: dict[str, int] = {}
    for index, record in enumerate(requests):
        if record.request_id in positions:
            first = positions[record.request_id]
            raise ResultValidationError(
                f"requests[{index}].request_id duplicates requests[{first}].request_id"
            )
        positions[record.request_id] = index
        _require(
            record.source == benchmark.workload.source,
            f"requests[{index}].source does not match benchmark workload",
        )
        _require(
            record.destination == benchmark.workload.destination,
            f"requests[{index}].destination does not match benchmark workload",
        )


def validate_complete_bundle(
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    requests: Sequence[RequestResult],
    metrics: Sequence[MetricRow],
    summary: Summary,
) -> None:
    """Validate a complete canonical bundle in memory."""
    _require(manifest.status == "complete", "complete bundle has non-complete manifest")
    _validate_manifest_identity(benchmark, manifest)
    _validate_requests(benchmark, manifest, requests)
    _require(
        len(requests) == benchmark.workload.request_count,
        "complete bundle must contain exactly one record per planned request",
    )

    metric_positions: dict[str, int] = {}
    for index, row in enumerate(metrics):
        if row.metric_id in metric_positions:
            first = metric_positions[row.metric_id]
            raise ResultValidationError(
                f"metrics[{index}].metric_id duplicates metrics[{first}].metric_id"
            )
        metric_positions[row.metric_id] = index
    _require(
        set(metric_positions) == set(benchmark.requested_metrics),
        "metrics.csv metric IDs do not match benchmark requested_metrics",
    )

    _require(
        summary.run_id == manifest.run_id, "summary.run_id does not match manifest"
    )
    _require(
        summary.status == manifest.status, "summary.status does not match manifest"
    )
    rows = {row.metric_id: row for row in metrics}
    for metric_id, value in summary.metrics.items():
        _require(metric_id in rows, f"summary.metrics.{metric_id} has no metric row")
        row = rows[metric_id]
        _require(
            value is None or row.value is not None,
            f"summary.metrics.{metric_id} supplies a value for an unavailable metric",
        )
        if value is not None and row.value is not None:
            _require(
                math.isclose(value, row.value, rel_tol=1e-12, abs_tol=1e-12),
                f"summary.metrics.{metric_id} does not match metrics.csv",
            )


def validate_failed_bundle(
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    error: ErrorRecord,
    requests: Sequence[RequestResult] = (),
) -> None:
    """Validate a failed canonical bundle in memory."""
    _require(manifest.status == "failed", "failed bundle has non-failed manifest")
    _validate_manifest_identity(benchmark, manifest)
    _validate_requests(benchmark, manifest, requests)
    _require(bool(error.exception_type), "error.exception_type must not be empty")


def validate_bundle(
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    *,
    requests: Sequence[RequestResult] = (),
    metrics: Sequence[MetricRow] = (),
    summary: Summary | None = None,
    error: ErrorRecord | None = None,
) -> None:
    """Dispatch bundle validation according to the manifest status."""
    if manifest.status == "complete":
        _require(error is None, "complete bundle must not contain error.json")
        _require(summary is not None, "complete bundle requires summary.json")
        validate_complete_bundle(benchmark, manifest, requests, metrics, summary)
        return
    _require(not metrics, "failed bundle must not contain standard metrics")
    _require(summary is None, "failed bundle must not contain summary.json")
    _require(error is not None, "failed bundle requires error.json")
    validate_failed_bundle(benchmark, manifest, error, requests)
