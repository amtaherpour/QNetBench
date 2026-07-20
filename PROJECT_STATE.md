# QNetBench Project State

Last updated (UTC): 2026-07-20
Status: COMPLETE
Active checkpoint: 8 — Finite sweep, aggregate analysis, plots, and mock-pipeline release gate
Last completed checkpoint: 8 — Finite sweep, aggregate analysis, plots, and mock-pipeline release gate
Branch: `main`
Last good commit: `01c9ea31aba45b1f947e7ec521705cfb3c95b0ba` (independent-audit CI run 29709597153)
Working tree: clean after merge

## Release target

- Target version: `0.1.0a1`
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 frozen
- Result contract: 0.1 frozen
- Metrics contract: 0.1 frozen
- `mock_pipeline_ready`: true
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Python: CPython 3.12 on GitHub-hosted Ubuntu 24.04
- Install command: `python -m pip install -e ".[dev,plot]"`
- Real-simulator research environment: N/A

## Last passing commands

GitHub Actions independent-audit CI run 29709597153:

- editable development and plotting installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- all focused suites from contracts through catalog — passed
- sweep and analysis tests — passed
- full mock-pipeline gate test — passed
- installed CLI smoke for all four frozen benchmarks, the nine-run sweep, and both approved plots — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- All independently audited capabilities through Checkpoint 7.
- Strict SweepSpec v0.1 loading with approved scalar replacements and explicit seeds.
- Deterministic bounded cartesian expansion with a hard 100-run preflight cap.
- Sequential sweep execution through the existing adapter-neutral single-run pipeline.
- Validated child bundles, a sweep manifest, deterministic aggregate CSV, and exactly two approved plots.
- The checked-in sweep expands to nine unique execution hashes and completes end to end.
- The complete simulator-independent mock pipeline is independently audited and ready for real-backend research.

## What is intentionally not implemented

- Parallelism, resume, retries, conditional axes, random search, databases, dashboards, or real-simulator research/integration.

## Open blockers

- None.

## Frozen assumptions in force

- Files under `schemas/v0_1/` and `docs/contracts/` are unchanged since the final Checkpoint 1 audit.
- The four frozen benchmark files and hashes are unchanged since Checkpoint 7.
- Sweep axes replace only approved scalar benchmark paths.
- Sweep expansion is capped at 100 runs before execution; the checked-in sweep has nine.
- Mock outputs and aggregate trends are synthetic and are not physical claims.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_08_report.md`
- Independent audit: `docs/ai_handoff/checkpoint_08_independent_audit.md`
- Gate document: `docs/mock_pipeline_gate.md`
- Independent-audit CI run: 29709597153
- Checked-in sweep: `sweeps/v0_1/link_loss_small.yaml`

## Next allowed action

Execute Checkpoint 8.5 only: simulator portfolio and paper-strategy freeze. Do not create production real-simulator adapters during Checkpoint 8.5.
