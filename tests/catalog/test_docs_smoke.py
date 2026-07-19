from pathlib import Path

from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_documented_quickstart_commands_smoke(tmp_path: Path) -> None:
    guide = Path("docs/quickstart.md").read_text(encoding="utf-8")
    assert "qnetbench list" in guide
    assert "qnetbench validate benchmarks/v0_1/link_2_batch.yaml" in guide
    assert "--backend mock" in guide
    assert "qnetbench validate-result" in guide
    assert "qnetbench summarize" in guide

    assert runner.invoke(app, ["list"]).exit_code == 0
    output = tmp_path / "documented-run"
    run = runner.invoke(
        app,
        [
            "run",
            "benchmarks/v0_1/link_2_batch.yaml",
            "--backend",
            "mock",
            "--seed",
            "7",
            "--out",
            str(output),
        ],
    )
    assert run.exit_code == 0, run.output
    assert runner.invoke(app, ["validate-result", str(output)]).exit_code == 0
    assert runner.invoke(app, ["summarize", str(output)]).exit_code == 0
