# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 3 — Canonical result models and artifact bundle I/O
Last completed checkpoint: 3 — Canonical result models and artifact bundle I/O
Branch: `main`
Last good commit: `eafee05af0bde802f3439bbe30b1869dae5e08f8` (independent-audit CI run 29698162327)
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

GitHub Actions independent-audit CI run 29698162327:

- `python -m pip install -e ".[dev]"` — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- `python -m pytest -q tests/contracts` — passed
- `python -m pytest -q tests/spec` — passed
- `python -m pytest -q tests/results tests/artifacts` — passed
- `python -m pytest -q` — passed
- `git diff --check` — passed

## What works now

- Frozen contracts and strict BenchmarkSpec runtime from Checkpoints 1–2.
- Strict canonical run, request, metric-row, summary, and error models implement Result Contract v0.1.
- Complete and failed bundles are safely read, cross-validated, written through temporary siblings, and revalidated before finalization.
- Duplicate or missing requests, count/hash mismatches, invalid times, malformed JSONL, non-finite values, and failed-run metric artifacts are rejected.
- Existing destinations require explicit overwrite; failed writes clean temporary output.
- Optional `events.jsonl` and `raw/` do not influence metric-independent validation.
- The merged Checkpoint 3 tree was independently revalidated after completion.

## What is intentionally not implemented

- Adapters, metric computation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Canonical result models implement frozen Contract v0.1 without schema changes.
- Complete bundles require one unique terminal record per planned request.
- Failed bundles contain no standard metrics.
- `events.jsonl` and `raw/` are optional and ignored by metric-independent validation.
- Existing output is never overwritten without explicit authorization.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_03_report.md`
- Independent audit: `docs/ai_handoff/checkpoint_03_independent_audit.md`
- Independent-audit CI run: 29698162327
- Complete fixture: `tests/fixtures/results/complete_run/`
- Failed fixture: `tests/fixtures/results/failed_run/`

## Next allowed action

Execute Checkpoint 4 only: adapter interface, registry, and deterministic mock adapter.

## Notes for the next agent

- Adapters must emit canonical records in memory and must not compute metrics or write final bundles.
- Do not add SeQUeNCe or any real simulator dependency during Checkpoint 4.
- Historical failed workflow notifications do not represent the independently audited merged Checkpoint 3 tree.
