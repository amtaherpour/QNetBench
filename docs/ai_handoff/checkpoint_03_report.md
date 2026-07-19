# Checkpoint 03 Report: Canonical result models and artifact bundle I/O

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-03-result-bundles`
Commit: CI-verified head `995f0ce9cb353f457e7119b63ee70a57ceb90b02`; completion metadata committed afterward
Previous good commit: `675e016f7431d40e0679e3945b4db74bfd211f68`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added strict canonical run manifest, request result, metric row, summary, and error models.
- Added cross-record validation for identity, hashes, counts, request uniqueness, metric rows, and summaries.
- Added safe JSON, JSONL, CSV, and benchmark readers with file and line context.
- Added temporary-sibling validated writes, explicit overwrite handling, and cleanup after failed finalization.
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
- `PROJECT_STATE.md`: recorded Checkpoint 3 completion and authorized Checkpoint 4 only.

## Tests added or changed

- Request invariants: time relations, latency identity, status-dependent fields, paths, non-finite values, duplicate IDs, and count mismatches.
- Bundle round trips: complete and failed layouts preserve normalized models and ignore optional `events.jsonl` and `raw/`.
- Bundle failures: malformed JSONL line context, missing files, invalid hashes, explicit overwrite, failed-run metrics rejection, finalization failure, and atomic cleanup.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29697824348.

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | 0 | Editable installation and dependencies passed. |
| `python -m ruff check .` | 0 | Lint passed. |
| `python -m ruff format --check .` | 0 | Formatting check passed. |
| `python -m pytest -q tests/contracts` | 0 | Frozen contract tests passed. |
| `python -m pytest -q tests/spec` | 0 | Specification tests passed. |
| `python -m pytest -q tests/results tests/artifacts` | 0 | Focused result/artifact tests passed; 20 passed in local pre-CI verification. |
| `python -m pytest -q` | 0 | Full repository test suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

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

Atomic-write strategy:

- write all files into a temporary sibling directory;
- read and validate the temporary bundle;
- rename it into place;
- for explicit overwrite, temporarily move the previous directory aside and restore it if finalization fails;
- remove temporary output after any failure.

Representative invariant failure: `requests[1].request_id duplicates requests[0].request_id`.

## Contract and architecture checks

- BenchmarkSpec changed: no.
- Canonical result contract changed: no; runtime implements frozen v0.1.
- Metric computation added: no.
- Optional `events.jsonl` and `raw/` influence validation: no.
- Existing destinations overwritten implicitly: no.

## Assumptions and decisions

- Summary metrics may be a validated subset of metric rows because the frozen example is a subset.
- Failed bundles may include validated partial request records when `written_request_count` records their exact count.
- Atomic directory replacement relies on same-filesystem sibling renames; platform-specific atomicity is limited by the host filesystem.

## Deviations from checkpoint plan

- The default CI includes an explicit focused result/artifact test step in addition to the full suite.

## Open issues and risks

- None blocking Checkpoint 4.

## PROJECT_STATE.md update

- Current checkpoint/result: Checkpoint 3 complete.
- Last passing evidence: GitHub Actions CI run 29697824348.
- Next allowed action: Checkpoint 4 only.

## Final status

STATUS: COMPLETE - Checkpoint 3 only. STOP. Next allowed checkpoint: 4.
