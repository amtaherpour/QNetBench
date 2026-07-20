"""Public-source qualification probe for QuISP without invoking OMNeT++."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    shutil.rmtree(arguments.work, ignore_errors=True)
    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "https://github.com/sfc-aqua/quisp.git",
            str(arguments.work),
        ],
        check=True,
    )
    readme = (arguments.work / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme.split())
    required_phrases = (
        "entanglement swapping",
        "taking data using it is still not fully implemented",
        "OMNeT++",
    )
    missing = [phrase for phrase in required_phrases if phrase not in normalized_readme]
    if missing:
        raise RuntimeError(f"QuISP README evidence changed; missing {missing}")
    if not (arguments.work / "simulation_tests").is_dir():
        raise RuntimeError("QuISP simulation_tests directory is unavailable")
    commit = subprocess.check_output(
        ["git", "-C", str(arguments.work), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    result = {
        "probe_schema_version": "1.0",
        "simulator_id": "quisp",
        "source_ref": "master",
        "source_commit": commit,
        "license_file_present": (arguments.work / "LICENSE").is_file(),
        "simulation_tests_present": True,
        "omnetpp_required": True,
        "swapping_output_collection_declared_incomplete": True,
        "runtime_build_attempted": False,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
