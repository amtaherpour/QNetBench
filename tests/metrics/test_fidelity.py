from qnetbench.metrics import compute_metrics
from tests.metrics.conftest import make_manifest, make_request


def test_complete_fidelity_coverage_is_computed() -> None:
    requests = (
        make_request("r1", fidelity=0.8),
        make_request("r2", fidelity=1.0),
    )
    rows = {
        row.metric_id: row for row in compute_metrics(make_manifest(requests), requests)
    }
    assert rows["fidelity_mean"].value == 0.9
    assert rows["fidelity_median"].value == 0.9
    assert rows["fidelity_mean"].coverage_count == 2


def test_partial_fidelity_coverage_is_unavailable() -> None:
    requests = (
        make_request("r1", fidelity=0.8),
        make_request("r2", fidelity=None),
    )
    row = compute_metrics(make_manifest(requests), requests, ["fidelity_mean"])[0]
    assert row.status == "unavailable"
    assert row.value is None
    assert row.population_count == 2
    assert row.coverage_count == 1
