"""Verify the public NetSquid access model without requesting credentials."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    request = urllib.request.Request(
        "https://netsquid.org/",
        headers={"User-Agent": "QNetBench-research-probe/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8", errors="replace")
    required = (
        "pypi.netsquid.org",
        "forum credentials",
        "requires registration",
    )
    missing = [phrase for phrase in required if phrase.lower() not in text.lower()]
    if missing:
        raise RuntimeError(f"NetSquid public access instructions changed: {missing}")
    result = {
        "probe_schema_version": "1.0",
        "simulator_id": "netsquid",
        "public_homepage_reachable": True,
        "registration_required": True,
        "private_package_index_documented": True,
        "package_install_attempted": False,
        "reason": "credentials and terms acceptance are user-specific",
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
