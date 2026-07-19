import json
from pathlib import Path

from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_validate_result_detects_corruption(tmp_path: Path) -> None:
    output = tmp_path / "run"
    run = runner.invoke(
        app,
        [
            "run",
            "examples/contracts/minimal_benchmark.yaml",
            "--backend",
            "mock",
            "--seed",
            "1",
            "--out",
            str(output),
        ],
    )
    assert run.exit_code == 0, run.output
    valid = runner.invoke(app, ["validate-result", str(output)])
    assert valid.exit_code == 0

    manifest_path = output / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["benchmark_hash"] = "f" * 64
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    invalid = runner.invoke(app, ["validate-result", str(output)])
    assert invalid.exit_code != 0
    assert "benchmark_hash" in invalid.stderr
