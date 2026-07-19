# Checkpoint 01 Report: Freeze the v0.1 contracts

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-01-contracts`
Commit: pending CI-verified head
Previous good commit: `6e692b73103f982ecf8d55159a6f28ead9a1fb32`
Active contract versions: benchmark 0.1 draft; result 0.1 draft; metrics 0.1 draft

## Scope completed

- Drafted normative BenchmarkSpec, canonical-result, and metric documents.
- Added six Draft 2020-12 JSON Schemas.
- Added minimal, complete-run, and failed-run examples.
- Added contract validation and negative-case tests.
- Added ADR-0001 defining contract and architecture boundaries.
- Added no production runtime behavior.

## Files created

- `docs/contracts/README.md`
- `docs/contracts/benchmark_spec_v0_1.md`
- `docs/contracts/canonical_result_v0_1.md`
- `docs/contracts/metric_definitions_v0_1.md`
- `schemas/v0_1/benchmark.schema.json`
- `schemas/v0_1/run_manifest.schema.json`
- `schemas/v0_1/request_result.schema.json`
- `schemas/v0_1/metric_row.schema.json`
- `schemas/v0_1/summary.schema.json`
- `schemas/v0_1/error.schema.json`
- `examples/contracts/minimal_benchmark.yaml`
- `examples/contracts/complete_run/benchmark.yaml`
- `examples/contracts/complete_run/run_manifest.json`
- `examples/contracts/complete_run/requests.jsonl`
- `examples/contracts/complete_run/metrics.csv`
- `examples/contracts/complete_run/summary.json`
- `examples/contracts/failed_run/run_manifest.json`
- `examples/contracts/failed_run/error.json`
- `docs/decisions/ADR-0001-contract-boundaries.md`
- `tests/contracts/test_contract_examples.py`
- `docs/ai_handoff/checkpoint_01_report.md`

## Files edited

- `pyproject.toml`: added PyYAML and jsonschema to the development extra.
- `PROJECT_STATE.md`: activated Checkpoint 1 and recorded the verification boundary.

## Tests added or changed

- `tests/contracts/test_contract_examples.py`: validates schemas/examples and rejects forbidden execution fields, unknown fields, duplicate IDs, invalid ranges, non-finite values, and invalid statuses.

## Commands run

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | pending | GitHub Actions verification pending. |
| `python -m ruff check .` | pending | GitHub Actions verification pending. |
| `python -m ruff format --check .` | pending | GitHub Actions verification pending. |
| `python -m pytest -q tests/contracts` | pending | GitHub Actions verification pending. |
| `python -m pytest -q` | pending | GitHub Actions verification pending. |
| `git diff --check` | pending | GitHub Actions verification pending. |

## Artifact evidence

- Normative schemas: `schemas/v0_1/*.schema.json`
- Examples: `examples/contracts/`

## Contract and architecture checks

- BenchmarkSpec backend-independent: yes.
- Canonical records and manifest are metric inputs: yes.
- Runtime production behavior added: no.
- Contract version frozen: pending CI verification.

## Assumptions and decisions

- JSON Schema Draft 2020-12 is used.
- Cross-record and cross-field invariants that JSON Schema cannot express portably are explicit contract rules and contract-test assertions.

## Deviations from checkpoint plan

- None.

## Open issues and risks

- CI verification pending.

## PROJECT_STATE.md update

- Current checkpoint/result: Checkpoint 1 in progress.
- Last passing command: Checkpoint 0 CI.
- Next allowed action: complete Checkpoint 1 verification only.

## Final status

STATUS: IN_PROGRESS — Checkpoint 1 verification pending. STOP.
