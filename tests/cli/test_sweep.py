from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_sweep_and_plot_commands_complete_and_reject_existing_output(
    tmp_path: Path,
) -> None:
    output = tmp_path / "sweep"
    args = [
        "sweep",
        "sweeps/v0_1/link_loss_small.yaml",
        "--backend",
        "mock",
        "--out",
        str(output),
    ]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert (output / "sweep_manifest.json").is_file()
    assert (output / "aggregate_metrics.csv").is_file()

    duplicate = runner.invoke(app, args)
    assert duplicate.exit_code != 0
    assert "already exists" in duplicate.stderr

    plotted = runner.invoke(app, ["plot", str(output)])
    assert plotted.exit_code == 0, plotted.output
    assert "request_success_probability.png" in plotted.stdout
    assert "latency_mean_s.png" in plotted.stdout


def test_sweep_help_has_no_resume_retry_parallel_or_overwrite_options() -> None:
    result = runner.invoke(app, ["sweep", "--help"])
    assert result.exit_code == 0
    for forbidden in ("resume", "retry", "parallel", "overwrite"):
        assert forbidden not in result.stdout.lower()
