from pathlib import Path

import pytest

from qnetbench.artifacts import read_bundle
from qnetbench.catalog import CatalogEntry, catalog_entries
from qnetbench.runners import RunRequest, run_single


@pytest.mark.parametrize("entry", catalog_entries(), ids=lambda entry: entry.filename)
def test_every_catalog_benchmark_runs_and_revalidates(
    entry: CatalogEntry,
    tmp_path: Path,
) -> None:
    output = tmp_path / entry.filename.removesuffix(".yaml")
    run_single(RunRequest(entry.path, "mock", 1, output))
    bundle = read_bundle(output)
    assert bundle.manifest.status == "complete"
    assert bundle.manifest.benchmark_id == entry.benchmark_id
    assert bundle.manifest.benchmark_hash == entry.benchmark_hash
    assert bundle.manifest.seed == 1
    assert len(bundle.requests) == entry.request_count
    assert len(bundle.metrics) == 8
