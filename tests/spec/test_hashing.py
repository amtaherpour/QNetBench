"""Deterministic normalization and benchmark hashing tests."""

from __future__ import annotations

from pathlib import Path

from qnetbench.spec import benchmark_hash, canonical_json, load_benchmark
from qnetbench.spec.models import BenchmarkSpec

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "spec"

# Frozen after calculating SHA-256 over the exact canonical JSON procedure.
MINIMAL_BENCHMARK_HASH = (
    "fa5b7b457debdb5dde5dd35fea3b5186511ed90cfd350327b5cf7ae837618d97"
)


def test_equivalent_sources_have_identical_canonical_json_and_hash() -> None:
    yaml_spec = load_benchmark(FIXTURES / "valid_equivalent.yaml")
    json_spec = load_benchmark(FIXTURES / "valid_equivalent.json")
    assert canonical_json(yaml_spec) == canonical_json(json_spec)
    assert benchmark_hash(yaml_spec) == benchmark_hash(json_spec)
    assert '"batch_start_s":0.0' in canonical_json(yaml_spec)


def test_meaningful_value_change_changes_hash() -> None:
    spec = load_benchmark(FIXTURES / "valid_equivalent.yaml")
    changed = spec.model_copy(
        update={
            "physical_profile": spec.physical_profile.model_copy(
                update={"memory_efficiency": 0.8}
            )
        }
    )
    assert benchmark_hash(changed) != benchmark_hash(spec)


def test_ordered_list_change_changes_hash() -> None:
    spec = load_benchmark(FIXTURES / "valid_equivalent.yaml")
    changed = spec.model_copy(
        update={"requested_metrics": tuple(reversed(spec.requested_metrics))}
    )
    assert benchmark_hash(changed) != benchmark_hash(spec)


def test_minimal_benchmark_golden_hash() -> None:
    source = ROOT / "examples" / "contracts" / "minimal_benchmark.yaml"
    spec: BenchmarkSpec = load_benchmark(source)
    assert benchmark_hash(spec) == MINIMAL_BENCHMARK_HASH
