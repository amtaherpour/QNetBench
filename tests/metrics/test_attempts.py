from qnetbench.metrics import compute_metrics
from tests.metrics.conftest import make_manifest, make_request


def test_attempts_per_success_uses_all_known_attempts() -> None:
    requests = (
        make_request("r1", attempts=1),
        make_request("r2", status="failed", attempts=3),
    )
    row = compute_metrics(make_manifest(requests), requests, ["attempts_per_success"])[
        0
    ]
    assert row.value == 4.0
    assert row.population_count == 2
    assert row.coverage_count == 2


def test_partial_attempt_coverage_is_unavailable() -> None:
    requests = (make_request("r1", attempts=1), make_request("r2", attempts=None))
    row = compute_metrics(make_manifest(requests), requests, ["attempts_per_success"])[
        0
    ]
    assert row.status == "unavailable"
    assert row.value is None
    assert row.population_count == 2
    assert row.coverage_count == 1


def test_zero_success_attempts_are_unavailable() -> None:
    requests = (make_request("r1", status="failed", attempts=2),)
    row = compute_metrics(make_manifest(requests), requests, ["attempts_per_success"])[
        0
    ]
    assert row.status == "unavailable"
