# Checkpoint 08.5 Report: Simulator portfolio and paper-strategy freeze

Status: COMPLETE
Date (UTC): 2026-07-20
Branch: `checkpoint-08-5-simulator-strategy`
CI-verified implementation head: `8ecaf4c705b008a3f81fe3d4e8928cb810fbbd87`
Core CI run: 29711718606
Previous good commit: `f04ec5e5361f6873a3a0286a2ce470710b7f2e61`

## Goal

Freeze a finite, evidence-based multi-simulator paper strategy after the
independently audited mock pipeline and before any production real adapter is
written.

## Frozen decisions

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

Checked-in JSON evidence and artifact digests are under `research/evidence/`.
These probes qualify research targets; they do not claim production adapter
support or frozen semantic mapping.

## Repository deliverables

- machine-readable portfolio and conformance profile;
- simulator landscape and compatibility/risk matrix;
- ADR-0002, ADR-0003, and ADR-0004;
- authoritative paper-track roadmap v1.0;
- executable/source/access probes and immutable JSON evidence;
- manual reproducibility workflows for every public probe;
- strategy/conformance tests integrated into core CI;
- updated project-control, README, and support-matrix documents.

## Quality evidence

Core CI run 29711718606 passed installation, Ruff lint/format, every accumulated
focused suite through the full mock pipeline, simulator-strategy tests, installed
CLI smoke, the full repository suite, and whitespace checks on Python 3.12.

Intermediate strategy verification exposed a brittle line-wrapped policy phrase.
The roadmap was clarified without weakening the test; the final core gate passed.
An earlier Q2NS tag assumption was corrected to the exact public main commit, and
the pinned full build/example probe passed before the portfolio was frozen.

## Scope exclusions

No production real adapter, cross-simulator numerical result, paper figure,
private credential, publication action, or frozen v0.1 change was added.

## Final status

STATUS: COMPLETE - Checkpoint 8.5 only. STOP. Next allowed action: independent audit, then Checkpoint 9.
