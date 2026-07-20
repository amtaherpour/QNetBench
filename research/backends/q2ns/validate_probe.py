"""Validate Q2NS research evidence against canonical request models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from qnetbench.results import RequestResult


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    evidence = json.loads(arguments.input.read_text(encoding="utf-8"))
    if evidence["simulator_id"] != "q2ns":
        raise RuntimeError("unexpected simulator ID")
    if evidence["same_seed_identical"] is not True:
        raise RuntimeError("same-seed evidence did not pass")
    summary: dict[str, object] = {
        "probe_schema_version": "1.0",
        "simulator_id": "q2ns",
        "q2ns_commit": evidence["q2ns_commit"],
        "ns3_commit": evidence["ns3_commit"],
        "cases": {},
    }
    cases = summary["cases"]
    if not isinstance(cases, dict):  # pragma: no cover - defensive
        raise RuntimeError("summary cases must be a mapping")
    for benchmark_id, case in evidence["cases"].items():
        normal = tuple(
            RequestResult.model_validate(row) for row in case["normal"]["records"]
        )
        failure = tuple(
            RequestResult.model_validate(row)
            for row in case["controlled_failure"]["records"]
        )
        alternate = tuple(
            RequestResult.model_validate(row)
            for row in case["alternate_seed"]["records"]
        )
        if len(normal) != 16 or len(failure) != 16 or len(alternate) != 16:
            raise RuntimeError(f"{benchmark_id}: expected 16 terminal records")
        normal_successes = sum(row.status == "success" for row in normal)
        failure_successes = sum(row.status == "success" for row in failure)
        if normal_successes < 1 or failure_successes != 0:
            raise RuntimeError(f"{benchmark_id}: success/failure evidence is invalid")
        canonical = json.dumps(
            case["normal"],
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        cases[benchmark_id] = {
            "record_count": len(normal),
            "normal_success_count": normal_successes,
            "controlled_failure_success_count": failure_successes,
            "normal_digest": hashlib.sha256(
                canonical.encode("utf-8")
            ).hexdigest(),
        }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
