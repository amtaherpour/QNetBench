"""Strict BenchmarkSpec v0.1 model tests."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from qnetbench.spec.models import BenchmarkSpec

ROOT = Path(__file__).resolve().parents[2]


def minimal_data() -> dict:
    return yaml.safe_load(
        (ROOT / "examples" / "contracts" / "minimal_benchmark.yaml").read_text(
            encoding="utf-8"
        )
    )


def test_model_accepts_frozen_minimal_contract() -> None:
    spec = BenchmarkSpec.model_validate(minimal_data())
    assert spec.schema_version == "0.1"
    assert spec.network.links[0].length_km == 10.0
    assert spec.requested_metrics[0] == "request_success_probability"


def test_unknown_field_is_rejected_with_field_path() -> None:
    data = minimal_data()
    data["network"]["nodes"][0]["unexpected"] = True
    with pytest.raises(ValidationError) as captured:
        BenchmarkSpec.model_validate(data)
    assert captured.value.errors()[0]["loc"] == ("network", "nodes", 0, "unexpected")


def test_invalid_range_is_rejected_with_field_path() -> None:
    data = minimal_data()
    data["physical_profile"]["memory_efficiency"] = 1.01
    with pytest.raises(ValidationError) as captured:
        BenchmarkSpec.model_validate(data)
    assert captured.value.errors()[0]["loc"] == (
        "physical_profile",
        "memory_efficiency",
    )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda data: data["network"]["nodes"].append({"node_id": "alice"}),
            "duplicates",
        ),
        (
            lambda data: data["network"]["links"].append(
                {
                    "link_id": "alice-bob",
                    "endpoints": ["alice", "bob"],
                    "length_km": 20.0,
                }
            ),
            "duplicates",
        ),
        (
            lambda data: data["network"]["links"][0].update(
                endpoints=["alice", "carol"]
            ),
            "unknown node_id",
        ),
        (
            lambda data: data["network"]["links"][0].update(
                endpoints=["alice", "alice"]
            ),
            "must differ",
        ),
        (lambda data: data["workload"].update(source="carol"), "unknown node_id"),
        (lambda data: data["workload"].update(deadline_s=0.0), "greater than 0"),
    ],
)
def test_cross_field_invariants_are_rejected(mutation, message: str) -> None:
    data = deepcopy(minimal_data())
    mutation(data)
    with pytest.raises(ValidationError, match=message):
        BenchmarkSpec.model_validate(data)


def test_duplicate_metric_ids_are_rejected() -> None:
    data = minimal_data()
    data["requested_metrics"].append(data["requested_metrics"][0])
    with pytest.raises(ValidationError, match="duplicate metric ID"):
        BenchmarkSpec.model_validate(data)


def test_strict_model_rejects_numeric_strings() -> None:
    data = minimal_data()
    data["physical_profile"]["memory_count_per_node"] = "2"
    with pytest.raises(ValidationError) as captured:
        BenchmarkSpec.model_validate(data)
    assert captured.value.errors()[0]["loc"] == (
        "physical_profile",
        "memory_count_per_node",
    )


def test_spec_package_has_no_forbidden_internal_imports() -> None:
    forbidden = {
        "qnetbench.adapters",
        "qnetbench.artifacts",
        "qnetbench.metrics",
        "qnetbench.results",
        "qnetbench.runners",
    }
    for path in sorted((ROOT / "qnetbench" / "spec").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any(
            module == prefix or module.startswith(f"{prefix}.")
            for module in imported
            for prefix in forbidden
        ), f"forbidden import in {path}"
