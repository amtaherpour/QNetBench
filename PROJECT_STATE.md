# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Last completed checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Branch: `checkpoint-07-catalog`
Last good commit: `c9163111d65d2b1d945a6a947824fa2594344f27` (CI run 29700632114)
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

GitHub Actions CI run 29700632114:

- editable development installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- all focused suites from contracts through runners/CLI — passed
- catalog and `list` tests — passed
- installed four-benchmark catalog CLI smoke — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- Checkpoints 0–6 capabilities.
- Exactly four static v0.1 benchmarks, stable catalog discovery, and the `list` command.
- All four benchmarks validate, execute through the deterministic mock single-run pipeline, and produce bundles that revalidate.
- Frozen IDs, scientific values, request counts, topology choices, and normalized hashes are recorded.
- User documentation describes only implemented mock behavior and marks SeQUeNCe not started.

## What is intentionally not implemented

- Sweeps, aggregation, plots, and SeQUeNCe research or integration.

## Open blockers

- None.

## Frozen assumptions in force

- The four benchmark files, identifiers, values, and recorded hashes are frozen after Checkpoint 7.
- All benchmark extensions are empty; backend, seed, output, and sweep concerns remain external.
- Grid routing uses the lexicographically smallest equal-length shortest path.
- `mock_pipeline_ready` remains false until the independent Checkpoint 8 gate.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_07_report.md`
- CI run: 29700632114
- Catalog: `benchmarks/v0_1/`
- Hash registry: `benchmarks/v0_1/README.md`

## Next allowed action

Perform a cumulative post-Checkpoint-7 audit only. Do not begin Checkpoint 8 until that audit is green and recorded.

## Notes for the next agent

- Re-run the entire accumulated Python 3.12 quality gate from merged `main`.
- Keep `mock_pipeline_ready` false; Checkpoint 8 has not started.
