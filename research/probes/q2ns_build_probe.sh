#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 WORK_DIRECTORY OUTPUT_JSON" >&2
  exit 2
fi

work_directory="$1"
output_json="$2"
rm -rf "$work_directory"
mkdir -p "$work_directory"

git clone --depth 1 --branch ns-3.47 https://gitlab.com/nsnam/ns-3-dev.git "$work_directory/ns-3"
git clone --depth 1 --branch main https://github.com/QuantumInternet-it/q2ns.git "$work_directory/ns-3/contrib/q2ns"

ns3_sha="$(git -C "$work_directory/ns-3" rev-parse HEAD)"
q2ns_sha="$(git -C "$work_directory/ns-3/contrib/q2ns" rev-parse HEAD)"

pushd "$work_directory/ns-3" >/dev/null
./ns3 configure --enable-examples --enable-tests
./ns3 build
./ns3 run q2ns-1-basics-example | tee "$work_directory/q2ns-example.log"
popd >/dev/null

python3 - "$output_json" "$ns3_sha" "$q2ns_sha" "$work_directory/q2ns-example.log" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

output = Path(sys.argv[1])
log_path = Path(sys.argv[4])
result = {
    "probe_schema_version": "1.0",
    "simulator_id": "q2ns",
    "q2ns_ref": "main",
    "q2ns_commit": sys.argv[3],
    "ns3_ref": "ns-3.47",
    "ns3_commit": sys.argv[2],
    "configure_completed": True,
    "build_completed": True,
    "example": "q2ns-1-basics-example",
    "example_completed": True,
    "example_log_bytes": log_path.stat().st_size,
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
PY
