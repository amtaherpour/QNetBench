# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 2 — Benchmark loading, normalization, and hashing
Last completed checkpoint: 1 — Freeze the v0.1 contracts
Branch: `checkpoint-02-spec-runtime`
Last good commit: `37f032009b5b37246d73b9185f7dc50f3c94cc92`
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

- Checkpoint 1 final-audit CI run 29696471826 passed.
- Checkpoint 2 local development checks passed on Python 3.13.5; Python 3.12 CI pending.

## What works now

- Frozen v0.1 contracts and examples from Checkpoint 1.
- Strict BenchmarkSpec runtime models, safe YAML/JSON loading, canonical JSON, and SHA-256 hashing are implemented on the checkpoint branch.
- Equivalent YAML/JSON fixtures and a golden minimal-benchmark hash are tested locally.

## What is intentionally not implemented

- Result artifacts, adapters, metrics implementation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; Checkpoint 2 Python 3.12 CI verification pending.

## Frozen assumptions in force

- Runtime models implement the frozen BenchmarkSpec v0.1 without schema changes.
- Unknown fields and unsafe YAML constructors are rejected.
- Canonical hashing uses compact sorted-key UTF-8 JSON and lowercase SHA-256.
- Backend, result, and metric modules are not imported by `qnetbench.spec`.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_02_report.md`
- Golden hash: `tests/spec/test_hashing.py`
- Equivalent fixtures: `tests/fixtures/spec/valid_equivalent.yaml` and `.json`

## Next allowed action

Complete Checkpoint 2 verification only. Do not begin Checkpoint 3 until all required commands pass and the report is complete.

## Notes for the next agent

- Do not change frozen schemas to make implementation easier.
- Do not add result, adapter, metric, runner, or CLI behavior during Checkpoint 2.
