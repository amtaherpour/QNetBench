#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 WORK_DIRECTORY OUTPUT_DIRECTORY" >&2
  exit 2
fi

work_directory="$1"
output_directory="$2"
rm -rf "$work_directory"
mkdir -p "$work_directory" "$output_directory"

git clone https://github.com/sfc-aqua/quisp.git "$work_directory/quisp"
git -C "$work_directory/quisp" checkout 2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c
commit="$(git -C "$work_directory/quisp" rev-parse HEAD)"
[[ "$commit" == "2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c" ]]

pushd "$work_directory/quisp" >/dev/null
pip install -r requirements.txt
make eigen
make exe
pytest -s -k NoErrorMIM simulation_tests | tee "$OLDPWD/$output_directory/quisp_no_error_mim.log"
popd >/dev/null

python3 - "$output_directory/quisp_qualification.json" \
  "$output_directory/quisp_no_error_mim.log" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

output = Path(sys.argv[1])
log_path = Path(sys.argv[2])
log = log_path.read_text(encoding="utf-8")
if "NoErrorMIM" not in log or "passed" not in log:
    raise RuntimeError("QuISP NoErrorMIM evidence is incomplete")
result = {
    "probe_schema_version": "1.0",
    "simulator_id": "quisp",
    "source_commit": "2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c",
    "headless_build_completed": True,
    "no_error_mim_test_completed": True,
    "no_error_mim_log_bytes": log_path.stat().st_size,
    "multi_hop_swapping_output_qualified": False,
    "promotion_decision": "not_promoted",
    "promotion_reason": "upstream swapping data collection is not fully implemented and no stable canonical terminal extraction was verified",
}
output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
PY
