from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from qnetbench.adapters import Adapter, BackendIdentity, SupportReport
from qnetbench.adapters.registry import register_adapter
from qnetbench.artifacts import read_bundle
from qnetbench.errors import ArtifactError, RunError
from qnetbench.runners import RunRequest, execution_hash, run_single
from qnetbench.spec import benchmark_hash, load_benchmark

BENCHMARK = Path("examples/contracts/minimal_benchmark.yaml")


class ExplodingAdapter(Adapter):
    @property
    def identity(self) -> BackendIdentity:
        return BackendIdentity("explode", "0.1", "explode", "test")

    def check_support(self, benchmark):  # type: ignore[no-untyped-def]
        return SupportReport(True, (), (), (), self.identity)

    def _run_supported(self, benchmark, *, benchmark_hash, seed):  # type: ignore[no-untyped-def]
        raise RuntimeError("synthetic adapter explosion")


def test_single_run_writes_valid_complete_bundle(tmp_path: Path) -> None:
    output = tmp_path / "run"
    run_single(RunRequest(BENCHMARK, "mock", 1, output))
    bundle = read_bundle(output)
    spec = load_benchmark(BENCHMARK)
    assert bundle.manifest.status == "complete"
    assert bundle.manifest.seed == 1
    assert bundle.manifest.benchmark_hash == benchmark_hash(spec)
    assert bundle.manifest.adapter_name == "mock"
    assert bundle.manifest.backend_version == "1.0"
    assert len(bundle.requests) == spec.workload.request_count
    assert len(bundle.metrics) == len(spec.requested_metrics)


def test_execution_hash_is_stable_and_seed_sensitive() -> None:
    spec = load_benchmark(BENCHMARK)
    identity = BackendIdentity("mock", "0.1", "mock", "1.0")
    digest = benchmark_hash(spec)
    assert execution_hash(digest, identity, 7) == execution_hash(digest, identity, 7)
    assert execution_hash(digest, identity, 7) != execution_hash(digest, identity, 8)


def test_existing_output_requires_explicit_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "run"
    run_single(RunRequest(BENCHMARK, "mock", 1, output))
    with pytest.raises(ArtifactError, match="already exists"):
        run_single(RunRequest(BENCHMARK, "mock", 1, output))
    run_single(RunRequest(BENCHMARK, "mock", 2, output, overwrite=True))
    assert read_bundle(output).manifest.seed == 2


def test_adapter_failure_writes_valid_failed_bundle(tmp_path: Path) -> None:
    register_adapter("explode", ExplodingAdapter, replace=True)
    output = tmp_path / "failed"
    with pytest.raises(RunError, match="synthetic adapter explosion"):
        run_single(RunRequest(BENCHMARK, "explode", 1, output))
    bundle = read_bundle(output)
    assert bundle.manifest.status == "failed"
    assert bundle.error is not None
    assert bundle.error.stage == "execution"
    assert bundle.error.exception_type == "RuntimeError"


def test_support_rejection_writes_valid_failed_bundle(tmp_path: Path) -> None:
    data = yaml.safe_load(BENCHMARK.read_text(encoding="utf-8"))
    data["network"] = {
        "nodes": [{"node_id": "alice"}, {"node_id": "relay"}, {"node_id": "bob"}],
        "links": [
            {
                "link_id": "alice-relay",
                "endpoints": ["alice", "relay"],
                "length_km": 5.0,
            },
            {
                "link_id": "relay-bob",
                "endpoints": ["relay", "bob"],
                "length_km": 5.0,
            },
        ],
    }
    data["protocol"]["swapping"] = "none"
    source = tmp_path / "unsupported.yaml"
    source.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    output = tmp_path / "unsupported-run"
    with pytest.raises(RunError, match="protocol.swapping"):
        run_single(RunRequest(source, "mock", 1, output))
    bundle = read_bundle(output)
    assert bundle.manifest.status == "failed"
    assert bundle.error is not None
    assert bundle.error.stage == "support_check"
