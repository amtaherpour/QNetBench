from __future__ import annotations

from collections.abc import Sequence

import pytest

from qnetbench.results import RequestResult, RunManifest


def make_request(
    request_id: str,
    *,
    status: str = "success",
    latency: float = 1.0,
    fidelity: float | None = 0.9,
    attempts: int | None = 1,
) -> RequestResult:
    return RequestResult(
        request_id=request_id,
        source="alice",
        destination="bob",
        submitted_at_s=0.0,
        terminal_at_s=latency,
        status=status,
        latency_s=latency,
        fidelity=fidelity if status == "success" else None,
        attempts=attempts,
        path=("alice", "bob"),
        failure_reason=None if status == "success" else "synthetic failure",
        metadata={},
    )


def make_manifest(
    requests: Sequence[RequestResult],
    *,
    expected: int | None = None,
    measurement_start_s: float = 0.0,
    measurement_end_s: float = 10.0,
) -> RunManifest:
    count = len(requests) if expected is None else expected
    return RunManifest(
        result_schema_version="0.1",
        run_id="fixture-run",
        benchmark_id="fixture-benchmark",
        benchmark_hash="0" * 64,
        execution_hash="1" * 64,
        qnetbench_version="0.0.0.dev0",
        adapter_name="fixture",
        adapter_version="0.1",
        backend_name="fixture",
        backend_version=None,
        seed=1,
        status="complete",
        started_at_utc="2026-07-19T00:00:00Z",
        ended_at_utc="2026-07-19T00:00:01Z",
        measurement_start_s=measurement_start_s,
        measurement_end_s=measurement_end_s,
        expected_request_count=count,
        written_request_count=count,
        python_version="3.12",
        platform="fixture",
        warnings=(),
        support_report_digest="fixture",
    )


@pytest.fixture
def mixed_requests() -> tuple[RequestResult, ...]:
    return (
        make_request("r1", latency=1.0, fidelity=0.8, attempts=1),
        make_request("r2", latency=2.0, fidelity=0.9, attempts=2),
        make_request("r3", latency=3.0, fidelity=1.0, attempts=3),
        make_request("r4", status="failed", latency=4.0, fidelity=None, attempts=4),
    )
