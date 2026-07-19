from typer.testing import CliRunner

from qnetbench.catalog import catalog_entries
from qnetbench.cli import app

runner = CliRunner()


def test_list_command_is_stable_and_complete() -> None:
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0, result.output
    lines = result.stdout.strip().splitlines()
    assert lines[0] == "benchmark_id\tnodes\tlinks\trequests\tbenchmark_hash"
    assert [line.split("\t", 1)[0] for line in lines[1:]] == [
        entry.benchmark_id for entry in catalog_entries()
    ]
