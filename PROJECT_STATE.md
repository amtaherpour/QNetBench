# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Last completed checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Branch: `main`
Last good commit: `d4b851caa27ed99e0eea8138c7b7f06786b50d5a` (cumulative-audit CI run 29700754803)
Working tree: clean after merge

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

GitHub Actions cumulative-audit CI run 29700754803:

- editable development installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- contract, specification, result, artifact, adapter, metric, runner, CLI, and catalog tests — passed
- installed CLI listing and all four frozen mock benchmark run/validate/summarize sequences — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- Frozen v0.1 benchmark, result, and metric contracts.
- Strict benchmark loading, canonicalization, and benchmark hashing.
- Canonical complete and failed result bundles with validated atomic I/O.
- Deterministic synthetic mock adapter with structured support reports.
- Eight backend-independent standard metrics.
- Adapter-neutral single-run orchestration and exact provenance.
- CLI commands `list`, `validate`, `run`, `summarize`, and `validate-result`.
- Exactly four frozen catalog benchmarks, all validated and executed through mock.
- The complete repository through Checkpoint 7 has been independently revalidated.

## What is intentionally not implemented

- Sweeps, aggregation, plots, and SeQUeNCe research or integration.

## Open blockers

- None.

## Frozen assumptions in force

- Files under `schemas/v0_1/` and `docs/contracts/` are unchanged since the final Checkpoint 1 audit.
- The four benchmark files, identifiers, values, request counts, topology choices, and hashes are frozen.
- All benchmark extensions are empty; backend, seed, output, and sweep concerns remain external.
- Grid routing uses the lexicographically smallest equal-length shortest path.
- Mock values are synthetic and are not a physics baseline.
- `mock_pipeline_ready` remains false until Checkpoint 8 is completed.

## Latest checkpoint evidence

- Checkpoint report: `docs/ai_handoff/checkpoint_07_report.md`
- Cumulative audit: `docs/ai_handoff/checkpoint_07_cumulative_audit.md`
- Cumulative-audit CI run: 29700754803
- Catalog: `benchmarks/v0_1/`
- Hash registry: `benchmarks/v0_1/README.md`

## Next allowed action

Execute Checkpoint 8 only: finite sweep, aggregate analysis, plots, and the mock-pipeline release gate.

## Notes for the next agent

- Do not begin SeQUeNCe research before the Checkpoint 8 mock-pipeline gate is complete.
- Keep historical failed intermediate CI attempts distinct from the accepted green checkpoint heads.
