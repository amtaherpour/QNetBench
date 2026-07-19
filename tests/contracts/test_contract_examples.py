from __future__ import annotations

import csv
import json
import math
from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas" / "v0_1"
EXAMPLES = ROOT / "examples" / "contracts"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def assert_finite(value):
    if isinstance(value, float):
        assert math.isfinite(value)
    elif isinstance(value, dict):
        for item in value.values():
            assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            assert_finite(item)


def assert_benchmark_invariants(spec: dict) -> None:
    assert_finite(spec)
    nodes = [item["node_id"] for item in spec["network"]["nodes"]]
    links = [item["link_id"] for item in spec["network"]["links"]]
    if len(nodes) != len(set(nodes)):
        raise ValueError("duplicate node_id")
    if len(links) != len(set(links)):
        raise ValueError("duplicate link_id")
    node_set = set(nodes)
    for link in spec["network"]["links"]:
        if len(set(link["endpoints"])) != 2 or not set(link["endpoints"]) <= node_set:
            raise ValueError("invalid link endpoints")
    workload = spec["workload"]
    if workload["source"] not in node_set or workload["destination"] not in node_set:
        raise ValueError("unknown workload node")
    if workload["source"] == workload["destination"]:
        raise ValueError("source and destination must differ")
    if workload["deadline_s"] <= workload["batch_start_s"]:
        raise ValueError("deadline must follow batch start")


def minimal_benchmark() -> dict:
    return yaml.safe_load((EXAMPLES / "minimal_benchmark.yaml").read_text())


def test_all_schemas_are_valid():
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        Draft202012Validator.check_schema(load_json(path))


def test_minimal_benchmark_validates_and_invariants_hold():
    spec = minimal_benchmark()
    validator("benchmark.schema.json").validate(spec)
    assert_benchmark_invariants(spec)


@pytest.mark.parametrize("field", ["backend", "seed", "output", "sweep"])
def test_execution_fields_are_rejected(field):
    spec = minimal_benchmark()
    spec[field] = "forbidden"
    with pytest.raises(ValidationError):
        validator("benchmark.schema.json").validate(spec)


def test_complete_run_examples_validate():
    directory = EXAMPLES / "complete_run"
    validator("benchmark.schema.json").validate(
        yaml.safe_load((directory / "benchmark.yaml").read_text())
    )
    validator("run_manifest.schema.json").validate(
        load_json(directory / "run_manifest.json")
    )
    records = [
        json.loads(line)
        for line in (directory / "requests.jsonl").read_text().splitlines()
    ]
    for record in records:
        validator("request_result.schema.json").validate(record)
    assert len({record["request_id"] for record in records}) == len(records)
    with (directory / "metrics.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        normalized = {
            "metric_id": row["metric_id"],
            "status": row["status"],
            "value": None if row["value"] == "" else float(row["value"]),
            "unit": None if row["unit"] == "" else row["unit"],
            "population_count": int(row["population_count"]),
            "coverage_count": int(row["coverage_count"]),
        }
        validator("metric_row.schema.json").validate(normalized)
    validator("summary.schema.json").validate(load_json(directory / "summary.json"))


def test_failed_run_examples_validate():
    directory = EXAMPLES / "failed_run"
    manifest = load_json(directory / "run_manifest.json")
    validator("run_manifest.schema.json").validate(manifest)
    assert manifest["status"] == "failed"
    validator("error.schema.json").validate(load_json(directory / "error.json"))


def test_negative_contract_cases_fail_for_intended_reason():
    schema = validator("benchmark.schema.json")
    spec = minimal_benchmark()
    bad = deepcopy(spec)
    bad["physical_profile"]["memory_efficiency"] = 1.1
    with pytest.raises(ValidationError):
        schema.validate(bad)
    bad = deepcopy(spec)
    bad["unexpected"] = True
    with pytest.raises(ValidationError):
        schema.validate(bad)
    bad = deepcopy(spec)
    bad["network"]["nodes"].append({"node_id": "alice"})
    with pytest.raises(ValueError, match="duplicate node_id"):
        assert_benchmark_invariants(bad)
    bad = deepcopy(spec)
    bad["physical_profile"]["memory_frequency_hz"] = float("nan")
    with pytest.raises(AssertionError):
        assert_benchmark_invariants(bad)
    record = json.loads(
        (EXAMPLES / "complete_run" / "requests.jsonl").read_text().splitlines()[0]
    )
    record["status"] = "mystery"
    with pytest.raises(ValidationError):
        validator("request_result.schema.json").validate(record)


def test_docs_and_schemas_agree_on_stable_metric_shape():
    schema = load_json(SCHEMAS / "metric_row.schema.json")
    assert schema["required"] == [
        "metric_id",
        "status",
        "value",
        "unit",
        "population_count",
        "coverage_count",
    ]
    text = (ROOT / "docs" / "contracts" / "metric_definitions_v0_1.md").read_text()
    for column in schema["required"]:
        assert column in text
    for status in ("ok", "unavailable", "not_applicable"):
        assert status in text
