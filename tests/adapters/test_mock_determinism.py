from __future__ import annotations

import json
from pathlib import Path

from qnetbench.adapters import MOCK_ALGORITHM_VERSION, MockAdapter
from qnetbench.spec import benchmark_hash, load_benchmark


def _lines(seed: int) -> list[str]:
    benchmark = load_benchmark("examples/contracts/minimal_benchmark.yaml")
    run = MockAdapter().run(
        benchmark,
        benchmark_hash=benchmark_hash(benchmark),
        seed=seed,
    )
    return [
        json.dumps(
            record.model_dump(mode="json"),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        for record in run.requests
    ]


def test_seed_one_matches_intentional_golden_records() -> None:
    golden = Path("tests/fixtures/mock/golden_seed_1.jsonl").read_text(encoding="utf-8")
    assert "\n".join(_lines(1)) + "\n" == golden
    assert MOCK_ALGORITHM_VERSION == "1.0"


def test_same_inputs_are_byte_stable() -> None:
    assert _lines(1) == _lines(1)


def test_alternate_seed_changes_outcome_reproducibly() -> None:
    seed_one = _lines(1)
    seed_two = _lines(2)
    assert seed_two == _lines(2)
    assert seed_one != seed_two
