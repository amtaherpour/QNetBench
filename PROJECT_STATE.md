# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 1 — Freeze the v0.1 contracts
Last completed checkpoint: 1 — Freeze the v0.1 contracts
Branch: `checkpoint-01-contracts`
Last good commit: `99c7f087b585597fac8ba90050941fd228e8d38b` (CI run 29695800416)
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

- Python: CPython 3.12 on GitHub-hosted Ubuntu
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

GitHub Actions CI run 29695800416:

- editable development install — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- `python -m pytest -q` — passed
- `git diff --check` — passed

## What works now

- Six valid v0.1 JSON Schemas.
- Minimal benchmark, complete-run, and failed-run examples validate.
- Negative contract cases are rejected.
- Benchmark, canonical-result, and metric contracts are frozen for implementation.

## What is intentionally not implemented

- Runtime Pydantic models, loaders, hashing, adapters, metrics implementation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- BenchmarkSpec is backend-independent.
- Unknown fields are rejected.
- Canonical manifest and terminal request records are the only metric inputs.
- Breaking contract changes require explicit approval, an ADR, fixture updates, and versioning.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_01_report.md`
- CI run: 29695800416
- Examples: `examples/contracts/`
- Schemas: `schemas/v0_1/`

## Next allowed action

Execute Checkpoint 2 only: benchmark loading, normalization, and hashing.

## Notes for the next agent

- Implement the frozen contracts exactly; do not change schemas for convenience.
- No production runtime behavior was added in Checkpoint 1.
