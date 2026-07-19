import pytest

from qnetbench.errors import MetricComputationError
from qnetbench.metrics import METRIC_IDS, STANDARD_METRICS, compute_metrics
from tests.metrics.conftest import make_manifest, make_request


def test_registry_order_and_units_are_frozen() -> None:
    assert METRIC_IDS == (
        "request_success_probability",
        "latency_mean_s",
        "latency_median_s",
        "latency_p95_s",
        "fidelity_mean",
        "fidelity_median",
        "throughput_success_per_s",
        "attempts_per_success",
    )
    assert tuple(item.unit for item in STANDARD_METRICS) == (
        "1",
        "s",
        "s",
        "s",
        "1",
        "1",
        "success/s",
        "attempt/success",
    )


def test_unknown_or_duplicate_metric_ids_are_rejected() -> None:
    requests = (make_request("r1"),)
    manifest = make_manifest(requests)
    with pytest.raises(MetricComputationError, match="unknown metric ID"):
        compute_metrics(manifest, requests, ["not-a-metric"])
    with pytest.raises(MetricComputationError, match="duplicate metric ID"):
        compute_metrics(
            manifest,
            requests,
            ["request_success_probability", "request_success_probability"],
        )
