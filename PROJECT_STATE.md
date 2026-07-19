# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 4 — Adapter interface, registry, and deterministic mock adapter
Last completed checkpoint: 3 — Canonical result models and artifact bundle I/O
Branch: `checkpoint-04-mock-adapter`
Last good commit: `ee714b0093d9dff17a941d500af3abb39e66af3e`
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

- Python: CPython 3.12 required; Checkpoint 4 GitHub Actions verification pending
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 3 independent audit CI run 29698290634 passed the accumulated quality gate.
- Checkpoint 4 adapter checks pass in the development environment; Python 3.12 CI pending.

## What works now

- Frozen contracts, strict BenchmarkSpec runtime, and canonical result bundles from Checkpoints 1–3.
- Adapter interface, structured support reports, registry, and deterministic synthetic mock adapter are implemented on the checkpoint branch.
- Same benchmark hash, seed, and mock algorithm version produce byte-stable records; an alternate seed changes outcomes reproducibly.

## What is intentionally not implemented

- Metric computation, runners, CLI, benchmark catalog, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; Checkpoint 4 Python 3.12 CI verification pending.

## Frozen assumptions in force

- Adapters emit canonical records in memory and do not compute metrics or write final bundles.
- Mock output is synthetic and not a physics baseline.
- No real simulator dependency or `qnetbench/adapters/sequence.py` is present.
- Unsupported paths are reported before execution.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_04_report.md`
- Golden records: `tests/fixtures/mock/golden_seed_1.jsonl`
- Mock algorithm version: `1.0`

## Next allowed action

Complete Checkpoint 4 verification only. Do not begin Checkpoint 5 until the exact final branch head passes CI and completion evidence is recorded.

## Notes for the next agent

- Do not present mock values as physically meaningful.
- Do not add metrics or final bundle writing to adapters.
