# Checkpoint 08.5 Report: Simulator portfolio and paper-strategy freeze

Status: IN_PROGRESS
Date (UTC): 2026-07-20
Branch: `checkpoint-08-5-simulator-strategy`
Previous good commit: `f04ec5e5361f6873a3a0286a2ce470710b7f2e61`

## Goal

Freeze a finite, evidence-based multi-simulator paper strategy after the
independently audited mock pipeline and before any production real adapter is
written.

## Decisions frozen subject to final branch verification

- Mandatory open targets: SeQUeNCe 1.0.0 at commit
  `ffd7c837f932c7bdc9450cd211aaf75b4d6a99a5` and Q2NS at commit
  `f22ba28f437099ba3cf9956ca332ba5ce8bb14fd` on ns-3.47 commit
  `e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f`.
- Qualification reserve/possible third backend: QuISP at commit
  `2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c`.
- Optional credentialed reference: NetSquid BYO plugin/private CI.
- Mock remains a deterministic non-physical software oracle.
- Frozen v0.1 contracts and four benchmark files/hashes remain unchanged.
- The remaining finite roadmap is Checkpoints 9–12.

## Verified public probes

| Candidate | Evidence | Result |
|---|---|---|
| SeQUeNCe | workflow 29710405052; install 1.0.0, seed/timeline/request/topology API probe | passed |
| Q2NS | workflow 29710405058; full ns-3.47 configure/build and official basic example | passed |
| QuISP | workflow 29710405064; exact source/license/tests/upstream limitation probe | passed as source qualification only |
| NetSquid | workflow 29710405060; registration/private-index access-model probe | passed; package install intentionally not attempted |

The checked-in JSON evidence and artifact digests are under `research/evidence/`.
These probes qualify research targets; they do not claim production adapter
support or frozen semantic mapping.

## Repository deliverables

- `simulators/portfolio_v1.yaml`
- `simulators/conformance_v1.yaml`
- `docs/research/simulator_landscape_2026.md`
- `docs/research/simulator_compatibility_matrix.md`
- ADR-0002, ADR-0003, and ADR-0004
- `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`
- executable/source/access probes and immutable JSON evidence under `research/`
- isolated GitHub Actions probe workflows
- strategy/conformance tests

## Scope exclusions

No production real adapter, cross-simulator numerical result, paper figure,
private credential, publication action, or frozen v0.1 change belongs to this
checkpoint.

## Verification status

All four public probes passed. Final accumulated core and strategy verification
has been requested on the evidence-frozen branch head. Completion metadata,
merge, and independent audit remain pending.

## Final status

STATUS: IN_PROGRESS — final CI, completion metadata, merge, and independent audit pending.
