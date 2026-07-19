# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 0 — Repository control plane and minimal package skeleton
Last completed checkpoint: 0 — Repository control plane and minimal package skeleton
Branch: `checkpoint-00-ci-verification`
Last good commit: `361313deaae985875b695a837273c5f01c69db9b` (CI run 29673928221)
Working tree: clean after commit

## Release target

- Target version: `0.1.0a1`
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 draft
- Result contract: 0.1 draft
- Metrics contract: 0.1 draft
- `mock_pipeline_ready`: false
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Python: CPython 3.12.13
- Platform: GitHub-hosted Ubuntu 24.04.4 runner
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

GitHub Actions CI run 29673928221 on 2026-07-19:

- `python -m pip install -e ".[dev]"` — passed
- `python -m ruff check .` — passed; all checks passed
- `python -m ruff format --check .` — passed; 2 files already formatted
- `python -m pytest -q` — passed; 1 test passed
- `git diff --check` — passed

## What works now

- The package installs in editable mode.
- `qnetbench` imports successfully.
- `qnetbench.__version__` equals `0.0.0.dev0`.
- Default Python 3.12 CI passes installation, lint, formatting, tests, and whitespace checks.

## What is intentionally not implemented

- Contracts, schemas, runtime models, adapters, metrics, runners, CLI commands, benchmarks, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Package and CLI name: `qnetbench`.
- Python baseline: 3.12.
- Packaging: PEP 621, setuptools, and pip-based commands.
- License: BSD-3-Clause.
- Target release: `0.1.0a1` after Checkpoint 11.
- Core runtime dependencies are introduced only by the checkpoints that use them.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_00_report.md`
- CI run: 29673928221
- Representative artifacts: N/A
- Golden hashes: N/A

## Next allowed action

Execute Checkpoint 1 only: freeze the v0.1 contracts.

## Notes for the next agent

- The repository tree was rebuilt from scratch by explicit owner instruction.
- Do not infer that previous historical repository contents are current implementation state.
- Do not implement runtime models or product behavior during Checkpoint 1.
