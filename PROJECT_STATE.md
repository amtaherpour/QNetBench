# QNetBench Project State

Last updated (UTC): 2026-07-20
Status: IN_PROGRESS
Active checkpoint: 8.5 independent audit — Simulator portfolio and paper-strategy freeze
Last completed checkpoint: 8.5 — Simulator portfolio and paper-strategy freeze
Branch: `checkpoint-08-5-independent-audit`
Last good commit: `f4d5f3d1b4118ace6d95788e66322a2cbf842b8c` (final Checkpoint 8.5 branch CI run 29711954466)
Working tree: committed on audit branch

## Release target

- Original alpha target: `0.1.0a1`
- Paper-ready release target: to be versioned at Checkpoint 12
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 frozen
- Result contract: 0.1 frozen
- Metrics contract: 0.1 frozen
- `mock_pipeline_ready`: true
- `simulator_portfolio_frozen`: true
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Core: CPython 3.12 on GitHub-hosted Ubuntu 24.04, final Checkpoint 8.5 branch CI run 29711954466
- SeQUeNCe: public `sequence==1.0.0` installation/API probe, run 29710405052
- Q2NS: exact commit `f22ba28f437099ba3cf9956ca332ba5ce8bb14fd` on ns-3.47 commit `e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f`, full build/basic-example run 29710405058
- QuISP: source commit `2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c`, source qualification run 29710405064
- NetSquid: public access-model run 29710405060; package credentials were neither requested nor fabricated

## What works now

- The complete simulator-independent mock pipeline through Checkpoint 8 is independently audited.
- The simulator portfolio, conformance policy, exact public revisions, checked-in probe evidence, ADRs, and finite paper-track roadmap are merged.
- Required open targets are SeQUeNCe and Q2NS; QuISP is the qualification reserve and NetSquid is optional BYO/private CI.
- No production real-simulator adapter or frozen v0.1 change has been added.

## What is intentionally not implemented

- Real-backend semantic micro-scenarios, production adapters, cross-simulator results, private credentialed packages, or publication actions.

## Open blockers

- None; independent post-merge verification is pending.

## Frozen assumptions in force

- Files under `schemas/v0_1/` and `docs/contracts/` remain unchanged.
- The four frozen benchmark files and hashes remain unchanged.
- Mock outputs remain synthetic and non-physical.
- Numerical equality across independent simulators is not a conformance requirement.
- Real-adapter production is prohibited until Checkpoint 9 freezes exact semantic mappings.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_08_5_report.md`
- Audit: `docs/ai_handoff/checkpoint_08_5_independent_audit.md`
- Portfolio: `simulators/portfolio_v1.yaml`
- Conformance profile: `simulators/conformance_v1.yaml`
- Probe evidence: `research/evidence/`
- Paper-track roadmap: `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`

## Next allowed action

Complete the independent Checkpoint 8.5 audit only. Do not begin Checkpoint 9 until the merged strategy tree is independently green and recorded.
