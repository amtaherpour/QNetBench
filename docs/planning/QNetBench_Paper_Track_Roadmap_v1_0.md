# QNetBench Paper-Track Roadmap v1.0

Status: authoritative from Checkpoint 8.5 onward. The original control plan remains
historical authority for completed Checkpoints 0–8; this roadmap supersedes its
original Checkpoints 9–11.

## Objective and frozen baseline

Deliver an openly reproducible simulator-neutral benchmark standard, conforming
multi-simulator implementations, a reference corpus, and a paper-ready artifact.
The moat is frozen semantics, conformance tests, canonical artifacts, explicit
simulator mappings, reference data, and governance—not adapter count.

Checkpoints 0–8 remain frozen: contracts v0.1, four benchmark files/values/hashes,
metric semantics, bundle invariants, runner boundary, and mock-oracle behavior.

## Portfolio

- mandatory open targets: SeQUeNCe 1.0.0 at commit
  `ffd7c837f932c7bdc9450cd211aaf75b4d6a99a5` and Q2NS main at commit
  `f22ba28f437099ba3cf9956ca332ba5ce8bb14fd` on ns-3.47 commit
  `e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f`;
- qualification reserve/possible third backend: QuISP at commit
  `2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c`;
- optional credentialed reference: NetSquid BYO plugin/private CI;
- mock: deterministic non-physical software oracle.

## Checkpoint 9 — Backend research and semantic mapping freeze

Create pinned isolated environments and executable link-2/chain-3 micro-scenarios
for SeQUeNCe and Q2NS. Freeze every input, unit, seed, timing, fidelity, request,
status, attempts, path, and raw-extraction mapping. Add repeatability and
controlled-failure evidence. Qualify QuISP headless build/output and make its
promotion decision. Define the NetSquid BYO boundary; run a package probe only
with authorized credentials. Freeze conformance fixtures and decide whether v0.1
is sufficient or a separately versioned sidecar/v0.2 proposal is justified.

Exit: no guessed API, conversion, seed, fidelity definition, or extraction remains
for the mandatory open targets.

## Checkpoint 10 — Production open adapters

Use internal sub-gates 10A SeQUeNCe and 10B Q2NS. Each must produce validated
complete/failed canonical bundles for link-2 and chain-3, pass repeatability,
support, failure, isolated integration, conformance, and full regression gates.
Implement 10C QuISP only if promoted by Checkpoint 9. Keep 10D NetSquid optional,
separately installed, and absent from default CI.

Exit: at least SeQUeNCe and Q2NS pass `simulators/conformance_v1.yaml`.

## Checkpoint 11 — Scientific validation and reference corpus

Run matched frozen scenarios/seeds across all conforming real backends. Publish
canonical reference bundles, immutable provenance, metric coverage/unavailable
analysis, native/derived/unavailable/unsupported mapping tables, repeatability
and sensitivity studies, cross-simulator tables/figures, limitations, and
artifact runtime/size budgets. Numerical equality is not required; every paper
number must trace to a validated artifact and pinned environment.

## Checkpoint 12 — Paper-ready public release

Build/install the final package in clean environments; finish user, adapter,
conformance, reproducibility, governance, citation, license, changelog, and
release documentation; publish stable examples and contributor templates; and
prepare the paper methods, limitations, artifact appendix, and availability
statement. Archive software/reference data with persistent identifiers only after
explicit human publication approval.

Exit: `release_candidate_ready: true` and an independent party can reproduce the
open reference workflow without private access.

## Control

Every checkpoint gets a branch, report, final green head, merge, and independent
audit. Repo-controlled failures are repaired before advancing. External access
constraints are isolated to optional lanes while open work continues. Tests are
never weakened, v0.1 is never silently changed, and new top-level checkpoints
require explicit approval plus an ADR.
