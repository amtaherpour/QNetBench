import ast
from pathlib import Path

from qnetbench.adapters import MockAdapter
from qnetbench.catalog import CATALOG_FILENAMES, catalog_entries, catalog_root
from qnetbench.metrics import METRIC_IDS
from qnetbench.spec import benchmark_hash, load_benchmark

EXPECTED = {
    "link_2_batch.yaml": (
        "qnb-v0-1-link-2-batch",
        2,
        1,
        "none",
        "3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf",
    ),
    "chain_3_batch.yaml": (
        "qnb-v0-1-chain-3-batch",
        3,
        2,
        "sequential",
        "8f44be6e6310fda341a7efeb5921dfadd90cff76196b1efb3aa7c076447ac13b",
    ),
    "chain_5_batch.yaml": (
        "qnb-v0-1-chain-5-batch",
        5,
        4,
        "sequential",
        "caf650aeb6f0a396ba65043b10c9f2bd2f56989e53e3b15d553adbc0aa86dc93",
    ),
    "grid_3x3_batch.yaml": (
        "qnb-v0-1-grid-3x3-batch",
        9,
        12,
        "sequential",
        "4b982542ea2fe6ae094c764acb89fb16dc9ecd8cb78835f33b46f33179649900",
    ),
}


def test_catalog_contains_exactly_four_frozen_benchmarks() -> None:
    root = catalog_root()
    assert tuple(path.name for path in sorted(root.glob("*.yaml"))) == tuple(
        sorted(CATALOG_FILENAMES)
    )
    entries = catalog_entries()
    assert tuple(entry.filename for entry in entries) == CATALOG_FILENAMES
    assert len({entry.benchmark_id for entry in entries}) == 4
    assert len({entry.benchmark_hash for entry in entries}) == 4


def test_frozen_values_hashes_and_readme_are_consistent() -> None:
    readme = (catalog_root() / "README.md").read_text(encoding="utf-8")
    for entry in catalog_entries():
        benchmark_id, nodes, links, swapping, digest = EXPECTED[entry.filename]
        spec = load_benchmark(entry.path)
        assert entry.benchmark_id == benchmark_id
        assert entry.benchmark_hash == digest == benchmark_hash(spec)
        assert entry.node_count == nodes
        assert entry.link_count == links
        assert entry.request_count == 16
        assert spec.protocol.swapping == swapping
        assert spec.requested_metrics == METRIC_IDS
        assert spec.extensions == {}
        assert MockAdapter().check_support(spec).supported is True
        assert entry.filename in readme
        assert entry.benchmark_id in readme
        assert entry.benchmark_hash in readme


def test_grid_lexical_tie_break_is_frozen() -> None:
    entry = next(
        item for item in catalog_entries() if item.filename == "grid_3x3_batch.yaml"
    )
    spec = load_benchmark(entry.path)
    run = MockAdapter().run(spec, benchmark_hash=entry.benchmark_hash, seed=1)
    assert run.requests[0].path == ("n00", "n01", "n02", "n12", "n22")


def test_catalog_does_not_import_adapters_or_simulators() -> None:
    path = Path("qnetbench/catalog.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    assert not any(
        module == "qnetbench.adapters"
        or module.startswith("qnetbench.adapters.")
        or module == "sequence"
        or module.startswith("sequence.")
        for module in modules
    )
