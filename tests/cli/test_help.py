from typer.testing import CliRunner

from qnetbench.cli import app

runner = CliRunner()


def test_help_exposes_only_checkpoint_six_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("validate", "run", "summarize", "validate-result"):
        assert command in result.stdout
    assert " list " not in result.stdout
