from qnetbench.metrics import compute_metrics
from qnetbench.results import RequestResult
from tests.metrics.conftest import make_manifest, make_request


def test_latency_metrics_and_nearest_rank_p95(
    mixed_requests: tuple[RequestResult, ...],
) -> None:
    rows = {
        row.metric_id: row
        for row in compute_metrics(make_manifest(mixed_requests), mixed_requests)
    }
    assert rows["latency_mean_s"].value == 2.0
    assert rows["latency_median_s"].value == 2.0
    assert rows["latency_p95_s"].value == 3.0
    assert rows["latency_p95_s"].population_count == 3


def test_zero_success_latency_is_unavailable() -> None:
    requests = (make_request("r1", status="failed", fidelity=None),)
    rows = {
        row.metric_id: row
        for row in compute_metrics(make_manifest(requests), requests)
    }
    for metric_id in ("latency_mean_s", "latency_median_s", "latency_p95_s"):
        assert rows[metric_id].status == "unavailable"
        assert rows[metric_id].value is None
        assert rows[metric_id].population_count == 0
