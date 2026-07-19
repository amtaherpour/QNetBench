# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 3 — Canonical result models and artifact bundle I/O
Last completed checkpoint: 2 — Benchmark loading, normalization, and hashing
Branch: `checkpoint-03-result-bundles`
Last good commit: `675e016f7431d40e0679e3945b4db74bfd211f68`
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

- Python: CPython 3.12 required; GitHub Actions verification pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 2 CI run 29697202931 passed.
- Checkpoint 3 focused result/artifact tests pass locally on Python 3.13.5; Python 3.12 CI pending.

## What works now

- Frozen contracts and strict BenchmarkSpec runtime from Checkpoints 1–2.
- Canonical result models, cross-record validation, safe bundle readers, and atomic writers are implemented on the checkpoint branch.
- Complete and failed fixture bundles round-trip locally.

## What is intentionally not implemented

- Adapters, metric computation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; Checkpoint 3 Python 3.12 CI verification pending.

## Frozen assumptions in force

- Canonical result models implement frozen Contract v0.1 without schema changes.
- Complete bundles require one unique terminal record per planned request.
- Failed bundles contain no standard metrics.
- `events.jsonl` and `raw/` are optional and ignored by metric-independent validation.
- Existing output is never overwritten without explicit authorization.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_03_report.md`
- Complete fixture: `tests/fixtures/results/complete_run/`
- Failed fixture: `tests/fixtures/results/failed_run/`

## Next allowed action

Complete Checkpoint 3 verification only. Do not begin Checkpoint 4 until all required commands pass and the report is complete.

## Notes for the next agent

- Do not add adapters or metric computation during Checkpoint 3.
- Do not change frozen schemas for implementation convenience.
