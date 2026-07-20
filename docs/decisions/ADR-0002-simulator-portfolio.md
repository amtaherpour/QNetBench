# ADR-0002: Multi-simulator portfolio for the paper track

- Status: accepted
- Date: 2026-07-20
- Decision owners: QNetBench project
- Supersedes: the original post-Checkpoint-8 single-real-backend assumption

## Context

The original alpha plan required the mock oracle plus a narrow SeQUeNCe adapter.
That is sufficient for a software alpha but not the strongest demonstration of a
simulator-neutral benchmark standard. A durable community benchmark needs at
least two independently designed open real simulators, while preserving an open
reproducibility path and avoiding superficial adapter count.

## Decision

1. Keep the mock backend as a deterministic contract/pipeline oracle only.
2. Select SeQUeNCe 1.0.0 at source commit
   `ffd7c837f932c7bdc9450cd211aaf75b4d6a99a5` as the primary mature open target.
3. Select Q2NS main at commit `f22ba28f437099ba3cf9956ca332ba5ce8bb14fd`
   on ns-3.47 commit `e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f`
   as the mandatory architecturally independent open target, subject to
   Checkpoint 9 semantic conformance.
4. Qualify QuISP commit `2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c`
   as the designated reserve/possible third open backend. Promote it only after
   headless installation and machine-readable link/chain extraction are proven.
5. Support NetSquid only as an optional credentialed bring-your-own-installation
   plugin and private-CI lane. It cannot block or become a dependency of the
   openly reproducible core.
6. Defer QuNetSim, SimulaQron/NetQASM, QKDNetSim, and QuNet to future benchmark
   profiles whose semantics match their application, QKD, or routing focus.

## Consequences

- The paper core will aim to demonstrate portability across native Python and
  ns-3/C++ simulation architectures, not merely two similar wrappers.
- QNetBench will not require numerical equality between simulators. It will
  require common benchmark identity, common metrics, explicit semantic mapping,
  reproducible revisions/seeds, and validated canonical artifacts.
- QuISP provides a planned fallback if Q2NS cannot meet the frozen v0.1 semantic
  conformance gate; no silent contract change is allowed.
- NetSquid access or credentials cannot block the open release or the primary
  paper claim.
- Production adapter work is deferred until Checkpoint 9 completes executable
  micro-scenarios and freezes extraction/mapping details.

## Evidence

- machine-readable portfolio: `simulators/portfolio_v1.yaml`
- compatibility matrix: `docs/research/simulator_compatibility_matrix.md`
- checked-in probe evidence: `research/evidence/`
- executable probe sources: `research/probes/`
- probe workflows: `.github/workflows/*probe*.yml`
