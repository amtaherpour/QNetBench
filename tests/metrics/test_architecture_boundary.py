import ast
from pathlib import Path


def test_metrics_do_not_import_adapters_artifacts_or_simulators() -> None:
    forbidden = ("qnetbench.adapters", "qnetbench.artifacts", "sequence")
    for path in Path("qnetbench/metrics").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
        assert not any(
            module == blocked or module.startswith(blocked + ".")
            for module in modules
            for blocked in forbidden
        ), path
