# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 7 — Frozen benchmark catalog and user-facing mock documentation
Last completed checkpoint: 6 — Single-run orchestration and CLI
Branch: `checkpoint-07-catalog`
Last good commit: `1681918091c79e33b893e22f13316e41fa451e62`
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

- Python: CPython 3.12 required; Checkpoint 7 CI pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 6 final CI run 29700342792 passed the accumulated quality gate.
- Focused catalog, CLI-list, documentation-smoke, and four-case mock checks pass in development; Python 3.12 CI pending.

## What works now

- Checkpoints 0–6 capabilities.
- Exactly four static v0.1 benchmarks, stable catalog discovery, and the `list` command are implemented on the checkpoint branch.
- All four benchmarks validate and complete through the mock single-run pipeline.
- User documentation describes only implemented mock behavior and marks SeQUeNCe not started.

## What is intentionally not implemented

- Sweeps, aggregation, plots, and SeQUeNCe research or integration.

## Open blockers

- None; Checkpoint 7 Python 3.12 CI verification pending.

## Frozen assumptions in force

- The four benchmark files, identifiers, values, and recorded hashes freeze after this checkpoint.
- All benchmark extensions are empty; backend, seed, output, and sweep concerns remain external.
- Grid routing uses the lexicographically smallest equal-length shortest path.
- `mock_pipeline_ready` remains false until the independent Checkpoint 8 gate.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_07_report.md`
- Catalog: `benchmarks/v0_1/`
- Hash registry: `benchmarks/v0_1/README.md`

## Next allowed action

Complete Checkpoint 7 verification only. Do not begin Checkpoint 8 before the exact final branch head is green and cumulative evidence is recorded.
