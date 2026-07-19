# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 2 — Benchmark loading, normalization, and hashing
Last completed checkpoint: 2 — Benchmark loading, normalization, and hashing
Branch: `main`
Last good commit: `4258224206e62ad402d673e4fe21cabd452dbfd5` (CI run 29697121906)
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

GitHub Actions CI run 29697121906:

- `python -m pip install -e ".[dev]"` — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- `python -m pytest -q tests/contracts` — passed
- `python -m pytest -q tests/spec` — passed
- `python -m pytest -q` — passed
- `git diff --check` — passed

## What works now

- Frozen v0.1 contracts and examples from Checkpoint 1.
- Strict BenchmarkSpec runtime models conform to the frozen benchmark schema.
- Safe YAML/JSON loading returns one typed `BenchmarkSpec` or raises a path-aware `ConfigError`.
- Equivalent source formatting and mapping order produce identical canonical JSON and hashes.
- The minimal benchmark golden hash is `fa5b7b457debdb5dde5dd35fea3b5186511ed90cfd350327b5cf7ae837618d97`.
- Specification code has no imports from adapters, artifacts, metrics, results, runners, or simulators.

## What is intentionally not implemented

- Result artifacts, adapters, metrics implementation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Runtime models implement BenchmarkSpec v0.1 without schema changes.
- Unknown fields, invalid ranges, duplicate IDs, invalid references, non-finite values, and unsafe YAML constructors are rejected.
- Canonical hashing uses compact sorted-key UTF-8 JSON and lowercase SHA-256.
- Backend, seed, output, and sweep concerns remain outside BenchmarkSpec.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_02_report.md`
- CI run: 29697121906
- Golden hash: `tests/spec/test_hashing.py`
- Equivalent fixtures: `tests/fixtures/spec/valid_equivalent.yaml` and `.json`

## Next allowed action

Execute Checkpoint 3 only: canonical result models and artifact bundle I/O.

## Notes for the next agent

- Implement the frozen result contracts exactly; do not change schemas for convenience.
- Do not add adapters or metric computation during Checkpoint 3.
