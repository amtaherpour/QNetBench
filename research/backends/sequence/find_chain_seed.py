"""Temporarily discover a reproducible successful SeQUeNCe chain seed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mapping_probe import run_case


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum", type=int, default=128)
    arguments = parser.parse_args()
    benchmark = Path("benchmarks/v0_1/chain_3_batch.yaml")
    attempts: list[dict[str, int]] = []
    for seed in range(1, arguments.maximum + 1):
        payload = run_case(benchmark, seed=seed, controlled_failure=False)
        success_count = sum(
            record["status"] == "success" for record in payload["records"]
        )
        attempts.append({"seed": seed, "success_count": success_count})
        if success_count:
            result = {
                "benchmark_id": payload["benchmark_id"],
                "selected_seed": seed,
                "success_count": success_count,
                "canonical_digest": payload["canonical_digest"],
                "attempts": attempts,
            }
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            arguments.output.write_text(
                json.dumps(result, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            print(json.dumps(result, sort_keys=True))
            return
    raise RuntimeError(
        f"no successful chain seed found in 1..{arguments.maximum}: {attempts}"
    )


if __name__ == "__main__":
    main()
