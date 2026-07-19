from pathlib import Path

from qnetbench.adapters import BackendIdentity
from qnetbench.artifacts import read_bundle
from qnetbench.runners import RunRequest, execution_hash, make_run_id, run_single


def test_manifest_provenance_recomputes_from_scientific_inputs(tmp_path: Path) -> None:
    output = tmp_path / "run"
    run_single(
        RunRequest(
            Path("examples/contracts/minimal_benchmark.yaml"),
            "mock",
            17,
            output,
        )
    )
    manifest = read_bundle(output).manifest
    identity = BackendIdentity(
        manifest.adapter_name,
        manifest.adapter_version,
        manifest.backend_name,
        manifest.backend_version,
    )
    assert manifest.execution_hash == execution_hash(
        manifest.benchmark_hash,
        identity,
        manifest.seed,
    )
    assert manifest.run_id == make_run_id(
        manifest.benchmark_id,
        manifest.backend_name,
        manifest.seed,
        manifest.execution_hash,
    )
    assert len(manifest.support_report_digest) == 64
