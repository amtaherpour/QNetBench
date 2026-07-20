# QNetBench Project State

Last updated (UTC): 2026-07-20
Status: IN_PROGRESS
Active checkpoint: 8 — Finite sweep, aggregate analysis, plots, and mock-pipeline release gate
Last completed checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Branch: `checkpoint-08-mock-pipeline`
Last good commit: `8d872c8ba3c8bdae84c52755c160e139260cc5c8`
Working tree: committed on checkpoint branch

## Release target

- Target version: `0.1.0a1`
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 frozen
- Result contract: 0.1 frozen
- Metrics contract: 0.1 frozen
- `mock_pipeline_ready`: false
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Python: CPython 3.12 required; Checkpoint 8 CI pending
- Install command: `python -m pip install -e ".[dev,plot]"`
- Real-simulator research environment: N/A

## Last passing commands

- Checkpoint 7 cumulative-audit CI run 29700754803 passed the complete accumulated gate.
- Focused Checkpoint 8 development checks are prepared; authoritative Python 3.12 CI is pending.

## What works now

- All capabilities through the independently audited Checkpoint 7 baseline.
- Strict SweepSpec loading, bounded deterministic expansion, sequential sweep orchestration, aggregate analysis, and approved plotting are implemented on the checkpoint branch.
- The checked-in sweep plans nine unique mock executions.

## What is intentionally not implemented

- Parallelism, resume, retries, conditional axes, random search, databases, dashboards, or real-simulator research/integration.

## Open blockers

- None; Checkpoint 8 Python 3.12 gate pending.

## Frozen assumptions in force

- Files under `schemas/v0_1/` and `docs/contracts/` remain unchanged.
- The four frozen benchmark files and hashes remain unchanged.
- Sweep axes replace only approved scalar benchmark paths.
- Sweep expansion is capped at 100 runs before execution; the checked-in sweep has nine.
- `mock_pipeline_ready` stays false until the exact final gate passes.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_08_report.md`
- Gate document: `docs/mock_pipeline_gate.md`
- Checked-in sweep: `sweeps/v0_1/link_loss_small.yaml`

## Next allowed action

Complete Checkpoint 8 verification only. Do not begin real-simulator research until the exact final branch head is green, merged, independently re-audited, and recorded.
