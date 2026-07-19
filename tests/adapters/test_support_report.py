from __future__ import annotations

from qnetbench.adapters import MockAdapter, available_adapters, get_adapter
from qnetbench.spec import load_benchmark


def test_supported_report_is_structured_and_stable() -> None:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    report = MockAdapter().check_support(benchmark)
    assert report.supported is True
    assert report.reasons == ()
    assert report.unsupported_paths == ()
    assert "synthetic" in report.warnings[0]
    assert report.backend_identity.adapter_name == "mock"
    assert len(report.digest()) == 64


def test_unsupported_protocol_is_reported_before_execution() -> None:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    unsupported_protocol = benchmark.protocol.model_copy(
        update={"swapping": "sequential"}
    )
    unsupported = benchmark.model_copy(update={"protocol": unsupported_protocol})
    report = MockAdapter().check_support(unsupported)
    assert report.supported is False
    assert report.unsupported_paths == ("protocol.swapping",)
    assert "requires 'none'" in report.reasons[0]


def test_unsupported_extension_path_is_reported() -> None:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    unsupported = benchmark.model_copy(update={"extensions": {"vendor": {}}})
    report = MockAdapter().check_support(unsupported)
    assert report.supported is False
    assert "extensions" in report.unsupported_paths


def test_registry_exposes_only_mock_at_this_checkpoint() -> None:
    assert available_adapters() == ("mock",)
    assert isinstance(get_adapter("MOCK"), MockAdapter)
