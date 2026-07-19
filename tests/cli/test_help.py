from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_help_exposes_checkpoint_seven_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("list", "validate", "run", "summarize", "validate-result"):
        assert command in result.stdout
