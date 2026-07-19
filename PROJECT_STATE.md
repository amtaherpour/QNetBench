# QNetBench Project State

Last updated (UTC): 2026-07-19
Status: IN_PROGRESS
Active checkpoint: 1 — Freeze the v0.1 contracts
Last completed checkpoint: 0 — Repository control plane and minimal package skeleton
Branch: `checkpoint-01-contracts`
Last good commit: `6e692b73103f982ecf8d55159a6f28ead9a1fb32`
Working tree: committed on checkpoint branch

## Release target

- Target version: `0.1.0a1`
- Current package version: `0.0.0.dev0`
- Benchmark contract: 0.1 draft pending CI
- Result contract: 0.1 draft pending CI
- Metrics contract: 0.1 draft pending CI
- `mock_pipeline_ready`: false
- `sequence_research_verified`: false
- `release_candidate_ready`: false

## Environment last verified

- Python: CPython 3.12.13
- Platform: GitHub-hosted Ubuntu runner
- Install command: `python -m pip install -e ".[dev]"`
- SeQUeNCe revision/environment: N/A

## Last passing commands

- Checkpoint 0 CI run 29673928221 passed.
- Checkpoint 1 CI verification pending.

## What works now

- Minimal package skeleton from Checkpoint 0.
- Draft v0.1 benchmark, canonical-result, and metric contracts, schemas, examples, and contract tests are present on the checkpoint branch.

## What is intentionally not implemented

- Runtime Pydantic models, loaders, hashing, adapters, metrics implementation, runners, CLI, benchmarks, sweeps, plots, and SeQUeNCe integration.

## Open blockers

- None; CI verification pending.

## Frozen assumptions in force

- BenchmarkSpec is backend-independent.
- Unknown fields are rejected.
- Canonical manifest and terminal request records are the only metric inputs.
- Breaking contract changes require explicit approval and versioning.

## Latest checkpoint evidence

- Report: `docs/ai_handoff/checkpoint_01_report.md`
- Representative examples: `examples/contracts/`
- Normative schemas: `schemas/v0_1/`

## Next allowed action

Complete Checkpoint 1 verification only. Do not begin Checkpoint 2 until CI passes and the contracts are marked frozen.

## Notes for the next agent

- No production runtime behavior was added in Checkpoint 1.
