# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 6 — Single-run orchestration and CLI
Last completed checkpoint: 5 — Backend-independent metric engine
Branch: `checkpoint-06-runner-cli`
Last good commit: `185a8134f3f33ac22ec918b2bc4b150cf48e5be9`
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

- Python: CPython 3.12 required; Checkpoint 6 CI pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 5 final CI run 29699955879 passed the accumulated quality gate.
- Focused runner and CLI tests plus module-level CLI smoke pass in development; Python 3.12 CI pending.

## What works now

- Checkpoints 0–5 capabilities.
- Adapter-neutral single-run orchestration, execution hashes, run IDs, provenance manifests, metrics, summaries, and atomic bundles are implemented on the checkpoint branch.
- CLI commands `validate`, `run`, `summarize`, and `validate-result` are implemented.
- Support and execution failures produce validated failed bundles and nonzero exits.

## What is intentionally not implemented

- Benchmark catalog/list command, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; Checkpoint 6 Python 3.12 CI verification pending.

## Frozen assumptions in force

- Execution hashes include benchmark hash, backend identity, seed, and execution options but exclude timestamps and output paths.
- The runner is adapter-neutral and uses only registry-facing adapter APIs.
- Saved summaries are derived convenience data and never metric inputs.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_06_report.md`
- Focused tests: `tests/runners/` and `tests/cli/`

## Next allowed action

Complete Checkpoint 6 verification only. Do not begin Checkpoint 7 before the exact final head is green and recorded.
