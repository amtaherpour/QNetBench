from pathlib import Path

from typer.testing import CliRunner

from qnetbench.adapters.registry import register_adapter
from qnetbench.artifacts import read_bundle
from qnetbench.cli import app
from tests.runners.test_single_run import ExplodingAdapter

runner = CliRunner()


def test_run_mock_and_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "run"
    args = [
        "run",
        "examples/contracts/minimal_benchmark.yaml",
        "--backend",
        "mock",
        "--seed",
        "1",
        "--out",
        str(output),
    ]
    first = runner.invoke(app, args)
    assert first.exit_code == 0, first.output
    assert read_bundle(output).manifest.status == "complete"

    duplicate = runner.invoke(app, args)
    assert duplicate.exit_code != 0
    assert "already exists" in duplicate.stderr

    replaced = runner.invoke(app, [*args, "--overwrite"])
    assert replaced.exit_code == 0, replaced.output


def test_adapter_failure_has_nonzero_exit_and_failed_bundle(tmp_path: Path) -> None:
    register_adapter("explode-cli", ExplodingAdapter, replace=True)
    output = tmp_path / "failed"
    result = runner.invoke(
        app,
        [
            "run",
            "examples/contracts/minimal_benchmark.yaml",
            "--backend",
            "explode-cli",
            "--seed",
            "3",
            "--out",
            str(output),
        ],
    )
    assert result.exit_code != 0
    assert read_bundle(output).manifest.status == "failed"
