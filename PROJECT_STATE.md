# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 5 — Backend-independent metric engine
Last completed checkpoint: 5 — Backend-independent metric engine
Branch: `checkpoint-05-metrics`
Last good commit: `5714cd3a3abcb88a54e2944665bcca2c88c8df9a` (CI run 29699911257)
Working tree: clean after commit

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

- Python: CPython 3.12 on GitHub-hosted Ubuntu 24.04
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

GitHub Actions CI run 29699911257:

- editable development installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- frozen contract tests — passed
- specification tests — passed
- result and artifact tests — passed
- adapter tests — passed
- metric tests — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- Checkpoints 0–4 capabilities, including the deterministic synthetic mock adapter.
- The frozen v0.1 eight-metric registry and backend-independent metric engine.
- Explicit unavailable states, stable coverage/population counts, nearest-rank p95, and measurement-window handling.
- Metrics consume only canonical complete manifests and request records.

## What is intentionally not implemented

- Runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Metrics consume only a canonical complete run manifest and canonical request records.
- Metrics do not read summaries, events, raw output, adapters, or simulator objects.
- Metric IDs, units, populations, and edge-case semantics match contract v0.1.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_05_report.md`
- CI run: 29699911257
- Focused tests: `tests/metrics/`

## Next allowed action

Execute Checkpoint 6 only: single-run orchestration and CLI through the mock backend.

## Notes for the next agent

- The runner must remain adapter-neutral.
- Summary output is derived convenience data and never a metric source.
