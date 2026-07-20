# QNetBench Project State

Last updated (UTC): 2026-07-20
Status: IN_PROGRESS
Active checkpoint: 8.5 — Simulator portfolio and paper-strategy freeze
Last completed checkpoint: 8 — Finite sweep, aggregate analysis, plots, and mock-pipeline release gate
Branch: `checkpoint-08-5-simulator-strategy`
Last good commit: `f04ec5e5361f6873a3a0286a2ce470710b7f2e61`
Working tree: committed on strategy branch

## Release target

- Original alpha target: `0.1.0a1`
- Paper-ready release target: to be versioned at Checkpoint 12
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 frozen
- Result contract: 0.1 frozen
- Metrics contract: 0.1 frozen
- `mock_pipeline_ready`: true
- `simulator_portfolio_frozen`: false
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Core: CPython 3.12 on GitHub-hosted Ubuntu 24.04, CP8 audit run 29709597153
- SeQUeNCe probe: public `sequence==1.0.0` workflow passed
- Q2NS probe: pinned ns-3.47 build workflow in progress after repairing the nonexistent release-tag assumption
- QuISP probe: public-source qualification workflow passed
- NetSquid probe: public access-model workflow passed; package credentials were neither requested nor fabricated

## What works now

- The complete simulator-independent mock pipeline through Checkpoint 8 is independently audited.
- A machine-readable multi-simulator portfolio and adapter-conformance profile are under verification.
- The paper track selects SeQUeNCe and Q2NS as mandatory open targets, QuISP as qualification reserve, and NetSquid as an optional credentialed BYO lane.
- The revised finite roadmap contains Checkpoints 9–12 only.
- No production real-simulator adapter or frozen v0.1 change has been added.

## Work remaining in Checkpoint 8.5

- Complete and record the final Q2NS build/example probe.
- Freeze exact probe artifacts and simulator revisions.
- Complete strategy/documentation tests and the accumulated core gate.
- Finalize portfolio status, support matrix, checkpoint report, merge, and independent audit.

## Frozen assumptions in force

- Files under `schemas/v0_1/` and `docs/contracts/` remain unchanged.
- The four frozen benchmark files and hashes remain unchanged.
- Mock outputs remain synthetic and non-physical.
- Numerical equality across independent simulators is not a conformance requirement.
- Real-adapter production is prohibited until Checkpoint 9 freezes exact semantic mappings.

## Latest checkpoint evidence

- CP8 report: `docs/ai_handoff/checkpoint_08_report.md`
- CP8 independent audit: `docs/ai_handoff/checkpoint_08_independent_audit.md`
- Strategy portfolio: `simulators/portfolio_v1.yaml`
- Conformance profile: `simulators/conformance_v1.yaml`
- Paper-track roadmap: `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`

## Next allowed action

Complete Checkpoint 8.5 verification only. Do not begin Checkpoint 9 production or micro-scenario work until the portfolio is frozen, merged, and independently audited.
