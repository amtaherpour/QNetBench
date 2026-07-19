import ast
from pathlib import Path


def test_runner_is_adapter_neutral() -> None:
    tree = ast.parse(Path("qnetbench/runners/single.py").read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    assert "qnetbench.adapters.mock" not in modules
    assert "sequence" not in modules
