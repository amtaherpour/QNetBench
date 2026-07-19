from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_validate_success_and_invalid_field_path() -> None:
    good = runner.invoke(app, ["validate", "examples/contracts/minimal_benchmark.yaml"])
    assert good.exit_code == 0
    assert good.stdout.startswith("VALID qnb-v0-1-minimal ")

    bad = runner.invoke(
        app, ["validate", "tests/fixtures/spec/invalid_unknown_field.yaml"]
    )
    assert bad.exit_code != 0
    assert "backend" in bad.stderr
