# Simulator portfolio research probes

These are research-evidence tools, not production adapters. They are intentionally
isolated from `qnetbench/adapters/` and may not change frozen v0.1 contracts.

- `sequence_api_probe.py` installs and exercises the pinned public SeQUeNCe API,
  seed controls, timeline kernel, and request/topology surfaces.
- `q2ns_build_probe.sh` clones ns-3.47 plus Q2NS main, records exact commits,
  builds the module, and runs the official basic example.
- `quisp_source_probe.py` records the exact public source commit, license/test
  layout, OMNeT++ dependency, and upstream swapping-data limitation. It does not
  claim headless runtime conformance.
- `netsquid_access_probe.py` verifies the public registration/private-index access
  model without requesting, storing, or fabricating user credentials.

Each probe has a dedicated GitHub Actions workflow and uploads a JSON artifact.
Passing these probes qualifies a candidate for deeper Checkpoint 9 micro-scenario
research; it does not establish QNetBench semantic conformance or support.
