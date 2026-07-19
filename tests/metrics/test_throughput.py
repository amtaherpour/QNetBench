from qnetbench.metrics import compute_metrics
from tests.metrics.conftest import make_manifest, make_request


def test_throughput_uses_manifest_measurement_window() -> None:
    requests = (make_request("r1"), make_request("r2", status="failed"))
    row = compute_metrics(
        make_manifest(requests, measurement_start_s=2.0, measurement_end_s=6.0),
        requests,
        ["throughput_success_per_s"],
    )[0]
    assert row.value == 0.25
    assert row.unit == "success/s"


def test_zero_measurement_window_is_unavailable() -> None:
    requests = (make_request("r1"),)
    manifest = make_manifest(requests, measurement_start_s=2.0, measurement_end_s=2.0)
    row = compute_metrics(manifest, requests, ["throughput_success_per_s"])[0]
    assert row.status == "unavailable"
    assert row.value is None


def test_negative_measurement_window_is_unavailable_defensively() -> None:
    requests = (make_request("r1"),)
    manifest = make_manifest(requests).model_copy(
        update={"measurement_start_s": 3.0, "measurement_end_s": 2.0}
    )
    row = compute_metrics(manifest, requests, ["throughput_success_per_s"])[0]
    assert row.status == "unavailable"
    assert row.value is None
