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

git clone --depth 1 --branch ns-3.47 https://gitlab.com/nsnam/ns-3-dev.git "$work_directory/ns-3"
git clone https://github.com/QuantumInternet-it/q2ns.git "$work_directory/ns-3/contrib/q2ns"
git -C "$work_directory/ns-3/contrib/q2ns" checkout f22ba28f437099ba3cf9956ca332ba5ce8bb14fd

ns3_sha="$(git -C "$work_directory/ns-3" rev-parse HEAD)"
q2ns_sha="$(git -C "$work_directory/ns-3/contrib/q2ns" rev-parse HEAD)"
[[ "$ns3_sha" == "e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f" ]]
[[ "$q2ns_sha" == "f22ba28f437099ba3cf9956ca332ba5ce8bb14fd" ]]

cp research/backends/q2ns/qnetbench-q2ns-mapping-probe.cc \
  "$work_directory/ns-3/scratch/qnetbench-q2ns-mapping-probe.cc"

pushd "$work_directory/ns-3" >/dev/null
./ns3 configure --enable-examples --disable-tests
./ns3 build qnetbench-q2ns-mapping-probe
./ns3 run "qnetbench-q2ns-mapping-probe --output=$OLDPWD/$output_directory/q2ns_raw.json"
popd >/dev/null

python research/backends/q2ns/validate_probe.py \
  --input "$output_directory/q2ns_raw.json" \
  --output "$output_directory/q2ns_mapping_probe.json"
