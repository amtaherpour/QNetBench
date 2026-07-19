# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 0 — Repository control plane and minimal package skeleton
Last completed checkpoint: none
Branch: `main`
Last good commit: pending clean Checkpoint 0 verification
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

- Python: 3.12 via GitHub Actions, verification pending
- Platform: GitHub-hosted Ubuntu runner, verification pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Pending clean Checkpoint 0 CI verification.

## What works now

- Minimal `qnetbench` package skeleton exists.
- Package version is declared as `0.0.0.dev0`.
- Default CI is configured for Python 3.12.

## What is intentionally not implemented

- Contracts, schemas, runtime models, adapters, metrics, runners, CLI commands, benchmarks, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None. Checkpoint 0 verification is pending.

## Frozen assumptions in force

- Package and CLI name: `qnetbench`.
- Python baseline: 3.12.
- Packaging: PEP 621, setuptools, and pip-based commands.
- License: BSD-3-Clause.
- Target release: `0.1.0a1` after Checkpoint 11.
- Core runtime dependencies are introduced only by the checkpoints that use them.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_00_report.md`
- Representative artifacts: N/A
- Golden hashes: N/A

## Next allowed action

Complete Checkpoint 0 verification only. Do not begin Checkpoint 1 until the report and this state file record passing evidence.

## Notes for the next agent

- The repository tree was rebuilt from scratch by explicit owner instruction.
- Do not infer that previous historical repository contents are current implementation state.
