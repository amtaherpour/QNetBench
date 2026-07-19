# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 6 — Single-run orchestration and CLI
Last completed checkpoint: 6 — Single-run orchestration and CLI
Branch: `checkpoint-06-runner-cli`
Last good commit: `3f3008700ea9df06a2532d16a2f53ffc9767a777` (CI run 29700289691)
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

GitHub Actions CI run 29700289691:

- editable development installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- contract, specification, result/artifact, adapter, and metric tests — passed
- runner and CLI tests — passed
- installed `qnetbench` CLI smoke — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- Checkpoints 0–5 capabilities.
- Adapter-neutral single-run orchestration, execution hashes, run IDs, exact provenance manifests, metrics, summaries, and atomic bundles.
- CLI commands `validate`, `run`, `summarize`, and `validate-result`.
- Support and execution failures produce validated failed bundles and nonzero exits.
- Existing output is rejected unless overwrite is explicit.

## What is intentionally not implemented

- Benchmark catalog/list command, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Execution hashes include benchmark hash, backend identity, seed, and execution options but exclude timestamps and output paths.
- The runner is adapter-neutral and uses only registry-facing adapter APIs.
- Saved summaries are derived convenience data and never metric inputs.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_06_report.md`
- CI run: 29700289691
- Focused tests: `tests/runners/` and `tests/cli/`

## Next allowed action

Execute Checkpoint 7 only: frozen four-benchmark catalog and user-facing mock documentation.

## Notes for the next agent

- Checkpoint 7 may add the `list` command and exactly four frozen benchmark files.
- Do not add sweeps, plots, or SeQUeNCe behavior.
