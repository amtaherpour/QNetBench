"""Canonical request and bundle invariant tests."""

from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from qnetbench.errors import ResultValidationError
from qnetbench.results import (
    MetricRow,
    RequestResult,
    RunManifest,
    Summary,
    validate_complete_bundle,
)
from qnetbench.spec import benchmark_hash, load_benchmark

BENCHMARK_PATH = "examples/contracts/minimal_benchmark.yaml"


def manifest_data() -> dict[str, object]:
    benchmark = load_benchmark(BENCHMARK_PATH)
    return {
        "result_schema_version": "0.1",
        "run_id": "qnb-v0-1-minimal-mock-1-11111111",
        "benchmark_id": benchmark.benchmark_id,
        "benchmark_hash": benchmark_hash(benchmark),
        "execution_hash": "1" * 64,
        "qnetbench_version": "0.0.0.dev0",
        "adapter_name": "mock",
        "adapter_version": "0.1",
        "backend_name": "mock",
        "backend_version": "0.1",
        "seed": 1,
        "status": "complete",
        "started_at_utc": "2026-07-19T00:00:00Z",
        "ended_at_utc": "2026-07-19T00:00:01Z",
        "measurement_start_s": 0.0,
        "measurement_end_s": 1.0,
        "expected_request_count": 2,
        "written_request_count": 2,
        "python_version": "3.12.13",
        "platform": "test",
        "warnings": [],
        "support_report_digest": "supported",
    }


def request_data(request_id: str, terminal: float = 0.1) -> dict[str, object]:
    return {
        "request_id": request_id,
        "source": "alice",
        "destination": "bob",
        "submitted_at_s": 0.0,
        "terminal_at_s": terminal,
        "status": "success",
        "latency_s": terminal,
        "fidelity": 0.94,
        "attempts": 1,
        "path": ["alice", "bob"],
        "failure_reason": None,
        "metadata": {},
    }


def metric_rows() -> tuple[MetricRow, ...]:
    units = {
        "request_success_probability": "1",
        "latency_mean_s": "s",
        "latency_median_s": "s",
        "latency_p95_s": "s",
        "fidelity_mean": "1",
        "fidelity_median": "1",
        "throughput_success_per_s": "success/s",
        "attempts_per_success": "attempt/success",
    }
    return tuple(
        MetricRow(
            metric_id=metric_id,
            status="ok",
            value=0.5,
            unit=units[metric_id],
            population_count=2,
            coverage_count=2,
        )
        for metric_id in units
    )


def test_request_requires_consistent_terminal_times() -> None:
    bad = request_data("request-0001")
    bad["terminal_at_s"] = 0.05
    with pytest.raises(ValidationError, match="latency_s must equal"):
        RequestResult.model_validate(bad)


def test_request_rejects_nonfinite_values() -> None:
    bad = request_data("request-0001")
    bad["latency_s"] = float("inf")
    with pytest.raises(ValidationError):
        RequestResult.model_validate(bad)
    bad = request_data("request-0001")
    bad["metadata"] = {"score": float("nan")}
    with pytest.raises(ValidationError, match="non-finite"):
        RequestResult.model_validate(bad)


def test_status_dependent_fields_are_strict() -> None:
    bad = request_data("request-0001")
    bad["status"] = "failed"
    with pytest.raises(ValidationError, match="fidelity=null"):
        RequestResult.model_validate(bad)
    bad = request_data("request-0001")
    bad["failure_reason"] = "not actually successful"
    with pytest.raises(ValidationError, match="must not have failure_reason"):
        RequestResult.model_validate(bad)


def test_path_must_match_request_endpoints() -> None:
    bad = request_data("request-0001")
    bad["path"] = ["bob", "alice"]
    with pytest.raises(ValidationError, match=r"path\[0\]"):
        RequestResult.model_validate(bad)


def test_manifest_rejects_invalid_time_and_count_relations() -> None:
    bad = manifest_data()
    bad["ended_at_utc"] = "2026-07-18T23:59:59Z"
    with pytest.raises(ValidationError, match="must not precede"):
        RunManifest.model_validate(bad)
    bad = manifest_data()
    bad["written_request_count"] = 1
    with pytest.raises(ValidationError, match="complete manifest"):
        RunManifest.model_validate(bad)


def test_bundle_rejects_duplicate_request_ids() -> None:
    benchmark = load_benchmark(BENCHMARK_PATH)
    manifest = RunManifest.model_validate(manifest_data())
    requests = (
        RequestResult.model_validate(request_data("request-0001")),
        RequestResult.model_validate(request_data("request-0001", terminal=0.2)),
    )
    summary = Summary(
        result_schema_version="0.1",
        run_id=manifest.run_id,
        status="complete",
        metrics={},
    )
    with pytest.raises(ResultValidationError, match="duplicates"):
        validate_complete_bundle(
            benchmark,
            manifest,
            requests,
            metric_rows(),
            summary,
        )


def test_bundle_rejects_missing_request_and_count_mismatch() -> None:
    benchmark = load_benchmark(BENCHMARK_PATH)
    data = deepcopy(manifest_data())
    data["expected_request_count"] = 1
    data["written_request_count"] = 1
    manifest = RunManifest.model_validate(data)
    requests = (RequestResult.model_validate(request_data("request-0001")),)
    summary = Summary(
        result_schema_version="0.1",
        run_id=manifest.run_id,
        status="complete",
        metrics={},
    )
    with pytest.raises(ResultValidationError, match="benchmark workload"):
        validate_complete_bundle(
            benchmark,
            manifest,
            requests,
            metric_rows(),
            summary,
        )


def test_metric_availability_and_coverage_are_consistent() -> None:
    with pytest.raises(ValidationError, match="require a value"):
        MetricRow(
            metric_id="latency_mean_s",
            status="ok",
            value=None,
            unit="s",
            population_count=1,
            coverage_count=1,
        )
    with pytest.raises(ValidationError, match="coverage_count"):
        MetricRow(
            metric_id="latency_mean_s",
            status="unavailable",
            value=None,
            unit="s",
            population_count=1,
            coverage_count=2,
        )
