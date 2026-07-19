# Checkpoint 03 Report: Canonical result models and artifact bundle I/O

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-03-result-bundles`
Commit: pending CI-verified head
Previous good commit: `675e016f7431d40e0679e3945b4db74bfd211f68`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added strict canonical run manifest, request result, metric row, summary, and error models.
- Added cross-record validation for identity, hashes, counts, request uniqueness, metric rows, and summaries.
- Added safe JSON, JSONL, CSV, and benchmark readers with file and line context.
- Added temporary-sibling validated writes and explicit overwrite handling.
- Added complete and failed fixture layouts and round-trip/failure tests.
- Added no adapter or metric-computation behavior.

## Files created

- `qnetbench/results/__init__.py`
- `qnetbench/results/models.py`
- `qnetbench/results/validate.py`
- `qnetbench/artifacts/__init__.py`
- `qnetbench/artifacts/reader.py`
- `qnetbench/artifacts/writer.py`
- `tests/results/test_request_invariants.py`
- `tests/artifacts/test_bundle_roundtrip.py`
- `tests/artifacts/test_bundle_failures.py`
- `tests/fixtures/results/complete_run/`
- `tests/fixtures/results/failed_run/`
- `docs/ai_handoff/checkpoint_03_report.md`

## Files edited

- `qnetbench/errors.py`: added public result-validation and artifact errors.
- `.github/workflows/ci.yml`: added the exact Checkpoint 3 focused test command.
- `PROJECT_STATE.md`: activated Checkpoint 3 and recorded the verification boundary.

## Tests added or changed

- Request invariants: time relations, latency identity, status-dependent fields, paths, non-finite values, duplicate IDs, and count mismatches.
- Bundle round trips: complete and failed layouts preserve normalized models and ignore optional `events.jsonl` and `raw/`.
- Bundle failures: malformed JSONL line context, missing files, invalid hashes, explicit overwrite, failed-run metrics rejection, and atomic cleanup.

## Commands run

Local development environment: CPython 3.13.5. Authoritative Python 3.12 CI is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m ruff check qnetbench/results qnetbench/artifacts tests/results tests/artifacts` | 0 | Focused lint passed locally. |
| `python -m ruff format --check qnetbench/results qnetbench/artifacts tests/results tests/artifacts` | 0 | Focused formatting passed locally. |
| `python -m pytest -q tests/results tests/artifacts` | 0 | 19 tests passed locally. |
| `python -m pytest -q` | pending | Full Python 3.12 CI pending. |
| `git diff --check` | pending | Python 3.12 CI pending. |

## Artifact evidence

Complete fixture layout:

```text
tests/fixtures/results/complete_run/
  benchmark.yaml
  run_manifest.json
  requests.jsonl
  metrics.csv
  summary.json
  events.jsonl
  raw/backend.txt
```

Failed fixture layout:

```text
tests/fixtures/results/failed_run/
  benchmark.yaml
  run_manifest.json
  error.json
```

## Contract and architecture checks

- BenchmarkSpec changed: no.
- Canonical result contract changed: no; runtime implements frozen v0.1.
- Metric computation added: no.
- Optional `events.jsonl` and `raw/` influence validation: no.
- Existing destinations overwritten implicitly: no.

## Assumptions and decisions

- Temporary sibling directories are fully written and re-read before final rename.
- Explicit overwrite uses a temporary sibling backup so the previous destination can be restored if finalization fails.
- Summary metrics may be a validated subset of metric rows because the frozen example is a subset.

## Deviations from checkpoint plan

- The default CI includes an explicit focused result/artifact test step in addition to the full suite.

## Open issues and risks

- Python 3.12 CI verification pending.

## PROJECT_STATE.md update

- Current checkpoint/result: Checkpoint 3 in progress.
- Last passing evidence: local focused tests.
- Next allowed action: complete Checkpoint 3 verification only.

## Final status

STATUS: IN_PROGRESS — Checkpoint 3 verification pending. STOP.
