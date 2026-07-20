# QNetBench Project State

Last updated (UTC): 2026-07-20
Status: IN_PROGRESS
Active checkpoint: 9 — Verified backend research and semantic mapping freeze
Last completed checkpoint: 8.5 — Simulator portfolio and paper-strategy freeze
Branch: `checkpoint-09-semantic-mapping`
Last good commit: `ac0479fe1cfa954cc59f743918b10fca7e834512`
Working tree: committed on checkpoint branch

## Release target

- Paper-ready release target: to be versioned at Checkpoint 12
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 frozen
- Result contract: 0.1 frozen
- Metrics contract: 0.1 frozen
- `mock_pipeline_ready`: true
- `simulator_portfolio_frozen`: true
- `sequence_research_verified`: false
- `q2ns_research_verified`: false
- `quisp_promoted`: false
- `release_candidate_ready`: false

## Environment last verified

- Core: CPython 3.12, Checkpoint 8.5 independent-audit CI run 29712136563
- Real-backend Checkpoint 9 evidence: pending

## What works now

- All capabilities and strategy controls through independently audited Checkpoint 8.5.
- SeQUeNCe research mapping probe is implemented on the checkpoint branch.

## What is intentionally not implemented

- Production real-simulator adapters, cross-simulator reference results, private
  credentialed packages, or publication actions.

## Open blockers

- None; executable research verification is in progress.

## Frozen assumptions in force

- Contracts, schemas, four benchmark files/hashes, metric semantics, and mock
  behavior remain unchanged.
- Production adapters remain prohibited until this checkpoint freezes mappings.
- External credential constraints are isolated to optional lanes while open work
  continues.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_09_report.md`
- Portfolio: `simulators/portfolio_v1.yaml`
- Conformance profile: `simulators/conformance_v1.yaml`

## Next allowed action

Complete Checkpoint 9 research and semantic mapping only. Do not begin production adapters.
