# QNetBench Project State

Last updated (UTC): 2026-07-10 22:10
Status: COMPLETE
Active checkpoint: none
Last completed checkpoint: Checkpoint 0 - Repository control plane and minimal package skeleton
Branch: main
Last good commit: pending GitHub CI verification on latest main
Working tree: clean on GitHub main

## Release target
- Target version: 0.1.0a1
- Current package version: 0.0.0.dev0
- Benchmark contract: 0.1 draft
- Result contract: 0.1 draft
- Metrics contract: 0.1 draft
- mock_pipeline_ready: false
- sequence_research_verified: false
- release_candidate_ready: false

## Environment last verified
- Python: 3.12 target in CI
- Platform: GitHub Actions ubuntu-latest expected for default CI
- Install command: python -m pip install -e ".[dev]"
- SeQUeNCe revision/environment: N/A

## Last passing commands
- `python -m pip install -e ".[dev]"` - reported passing during Checkpoint 0 local/Codex execution
- `python -m ruff check .` - reported passing during Checkpoint 0 local/Codex execution
- `python -m ruff format --check .` - reported passing during Checkpoint 0 local/Codex execution
- `python -m pytest -q` - reported passing during Checkpoint 0 local/Codex execution
- `git diff --check` - reported passing during Checkpoint 0 local/Codex execution

## What works now
- Minimal package skeleton exists.
- `qnetbench` package imports.
- `qnetbench.__version__` is defined as `0.0.0.dev0`.
- Default CI workflow is present and targets Python 3.12.
- Planning Markdown files are present at repository root for Codex-readable context.

## What is intentionally not implemented
- Benchmark/result/metric contracts and JSON schemas
- Pydantic runtime models
- CLI commands
- Adapters, including mock and SeQUeNCe
- Metrics engine
- Runners
- Benchmark catalog
- Sweeps
- Plots
- Validation suite
- Release artifacts beyond the Checkpoint 0 skeleton

## Open blockers
- None for Checkpoint 0.
- Before starting Checkpoint 1, confirm GitHub CI passes on main.

## Frozen assumptions in force
- Package name is `qnetbench`.
- Target alpha version is `0.1.0a1` after Checkpoint 11.
- Current package version is `0.0.0.dev0`.
- Python baseline is 3.12.
- Build backend is normal setuptools via `setuptools.build_meta`.
- Developer workflow is pip, pytest, Ruff, and build.
- License is BSD-3-Clause.
- Work proceeds one checkpoint at a time.

## Latest checkpoint evidence
- Report: docs/ai_handoff/checkpoint_00_report.md
- Representative artifacts: N/A
- Golden hashes: N/A

## Next allowed action
Checkpoint 1 only: Freeze the v0.1 contracts.

## Notes for the next agent
- Do not start Checkpoint 1 until the human/controller confirms Checkpoint 0 cleanup is acceptable.
- Do not add runtime behavior while repairing Checkpoint 0 documentation.
- The root planning Markdown files are intentionally kept for Codex readability unless a later cleanup explicitly moves them.
