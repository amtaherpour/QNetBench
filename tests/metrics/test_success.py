from qnetbench.metrics import compute_metrics
from qnetbench.results import RequestResult
from tests.metrics.conftest import make_manifest


def test_success_probability_uses_all_planned_requests(
    mixed_requests: tuple[RequestResult, ...],
) -> None:
    row = compute_metrics(
        make_manifest(mixed_requests), mixed_requests, ["request_success_probability"]
    )[0]
    assert row.value == 0.75
    assert row.unit == "1"
    assert row.population_count == 4
    assert row.coverage_count == 4
