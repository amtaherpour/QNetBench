import json
from pathlib import Path

from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_summarize_reads_saved_bundle_without_rerun(tmp_path: Path) -> None:
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
    summary = runner.invoke(app, ["summarize", str(output)])
    assert summary.exit_code == 0
    payload = json.loads(summary.stdout)
    assert payload["status"] == "complete"
    assert "request_success_probability" in payload["metrics"]
