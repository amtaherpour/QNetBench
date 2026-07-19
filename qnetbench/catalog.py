"""Frozen v0.1 benchmark catalog discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from qnetbench.spec import benchmark_hash, load_benchmark

CATALOG_FILENAMES = (
    "link_2_batch.yaml",
    "chain_3_batch.yaml",
    "chain_5_batch.yaml",
    "grid_3x3_batch.yaml",
)


@dataclass(frozen=True)
class CatalogEntry:
    """Validated metadata for one frozen catalog benchmark."""

    filename: str
    path: Path
    benchmark_id: str
    title: str
    benchmark_hash: str
    node_count: int
    link_count: int
    request_count: int


def catalog_root() -> Path:
    """Return the repository's frozen v0.1 benchmark directory."""
    return Path(__file__).resolve().parents[1] / "benchmarks" / "v0_1"


def catalog_entries(root: str | Path | None = None) -> tuple[CatalogEntry, ...]:
    """Load the exactly four frozen benchmarks in stable presentation order."""
    directory = catalog_root() if root is None else Path(root)
    entries: list[CatalogEntry] = []
    for filename in CATALOG_FILENAMES:
        path = directory / filename
        spec = load_benchmark(path)
        entries.append(
            CatalogEntry(
                filename=filename,
                path=path,
                benchmark_id=spec.benchmark_id,
                title=spec.title,
                benchmark_hash=benchmark_hash(spec),
                node_count=len(spec.network.nodes),
                link_count=len(spec.network.links),
                request_count=spec.workload.request_count,
            )
        )
    identifiers = [entry.benchmark_id for entry in entries]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("catalog benchmark IDs must be unique")
    return tuple(entries)


__all__ = ["CATALOG_FILENAMES", "CatalogEntry", "catalog_entries", "catalog_root"]
