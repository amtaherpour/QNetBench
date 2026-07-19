from __future__ import annotations

import ast
from pathlib import Path

import pytest

from qnetbench.adapters import MockAdapter
from qnetbench.errors import UnsupportedBenchmarkError
from qnetbench.spec import benchmark_hash, load_benchmark


def test_mock_emits_one_canonical_terminal_record_per_request() -> None:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    run = MockAdapter().run(
        benchmark,
        benchmark_hash=benchmark_hash(benchmark),
        seed=2,
    )
    assert len(run.requests) == benchmark.workload.request_count
    assert run.measurement_start_s == benchmark.workload.batch_start_s
    assert run.measurement_end_s == benchmark.workload.deadline_s
    assert {record.request_id for record in run.requests} == {
        "request-0001",
        "request-0002",
    }
    for record in run.requests:
        assert record.source == benchmark.workload.source
        assert record.destination == benchmark.workload.destination
        assert record.path == ("alice", "bob")
        assert record.metadata["synthetic"] is True
        assert record.metadata["mock_algorithm_version"] == "1.0"


def test_run_rejects_unsupported_benchmark_before_execution() -> None:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    protocol = benchmark.protocol.model_copy(update={"swapping": "sequential"})
    unsupported = benchmark.model_copy(update={"protocol": protocol})
    with pytest.raises(UnsupportedBenchmarkError, match="protocol.swapping"):
        MockAdapter().run(
            unsupported,
            benchmark_hash=benchmark_hash(benchmark),
            seed=1,
        )


def test_adapter_modules_do_not_import_metrics_cli_analysis_or_artifacts() -> None:
    forbidden = {
        "qnetbench.metrics",
        "qnetbench.cli",
        "qnetbench.analysis",
        "qnetbench.artifacts",
    }
    for path in Path("qnetbench/adapters").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any(
            module == blocked or module.startswith(blocked + ".")
            for module in imported
            for blocked in forbidden
        ), path
