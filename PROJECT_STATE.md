# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 5 — Backend-independent metric engine
Last completed checkpoint: 4 — Adapter interface, registry, and deterministic mock adapter
Branch: `checkpoint-05-metrics`
Last good commit: `feaf0a424c30fb3eb2631bfc138da02fb2b1e678`
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

- Python: CPython 3.12 required; Checkpoint 5 CI pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 4 final CI run 29699665088 passed the accumulated quality gate.
- Focused Checkpoint 5 metric checks pass in the development environment; Python 3.12 CI pending.

## What works now

- Checkpoints 0–4 capabilities, including the deterministic synthetic mock adapter.
- The complete v0.1 metric registry and pure metric engine are implemented on the checkpoint branch.
- Explicit unavailable states, coverage counts, nearest-rank p95, and measurement-window handling are tested.

## What is intentionally not implemented

- Runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; Checkpoint 5 Python 3.12 CI verification pending.

## Frozen assumptions in force

- Metrics consume only a canonical complete run manifest and canonical request records.
- Metrics do not read summaries, events, raw output, adapters, or simulator objects.
- Metric IDs, units, populations, and edge-case semantics match contract v0.1.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_05_report.md`
- Focused tests: `tests/metrics/`

## Next allowed action

Complete Checkpoint 5 verification only. Do not begin Checkpoint 6 before the exact final head is green and recorded.
