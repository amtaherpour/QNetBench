# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: COMPLETE
Active checkpoint: 4 — Adapter interface, registry, and deterministic mock adapter
Last completed checkpoint: 4 — Adapter interface, registry, and deterministic mock adapter
Branch: `checkpoint-04-mock-adapter`
Last good commit: `bf7a4bc175cda21b8a8414d96b9b63153e95c912` (CI run 29699627204)
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

GitHub Actions CI run 29699627204:

- editable development installation — passed
- `python -m ruff check .` — passed
- `python -m ruff format --check .` — passed
- frozen contract tests — passed
- specification tests — passed
- result and artifact tests — passed
- adapter tests — passed
- full repository test suite — passed
- `git diff --check` — passed

## What works now

- Frozen contracts, strict BenchmarkSpec runtime, and canonical result bundles from Checkpoints 1–3.
- Adapter interface, structured support reports, registry, and deterministic synthetic mock adapter.
- Same benchmark hash, seed, and mock algorithm version produce byte-stable canonical records.
- Alternate seed behavior is reproducibly different.
- Unsupported protocol and extension paths are rejected before execution.

## What is intentionally not implemented

- Metric computation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None.

## Frozen assumptions in force

- Adapters emit canonical records in memory and do not compute metrics or write final bundles.
- Mock output is synthetic and not a physics baseline.
- No real simulator dependency or `qnetbench/adapters/sequence.py` is present.
- Unsupported paths are reported before execution.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_04_report.md`
- CI run: 29699627204
- Golden records: `tests/fixtures/mock/golden_seed_1.jsonl`
- Mock algorithm version: `1.0`

## Next allowed action

Execute Checkpoint 5 only: backend-independent metric engine.

## Notes for the next agent

- Metrics may consume only canonical manifests and request records.
- Metrics must not import adapters, artifacts, raw output, or simulator packages.
