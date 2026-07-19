# Checkpoint 02 Report: Benchmark loading, normalization, and hashing

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-02-spec-runtime`
Commit: pending CI-verified head
Previous good commit: `37f032009b5b37246d73b9185f7dc50f3c94cc92`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added strict Pydantic v2 models matching BenchmarkSpec v0.1.
- Added safe YAML/JSON loading with typed, path-aware `ConfigError` failures.
- Added deterministic normalized JSON and lowercase SHA-256 hashing.
- Added equivalent-source, strictness, unsafe-YAML, and golden-hash tests.
- Added no result, adapter, metric, runner, or CLI behavior.

## Files created

- `qnetbench/errors.py`
- `qnetbench/spec/__init__.py`
- `qnetbench/spec/models.py`
- `qnetbench/spec/loader.py`
- `qnetbench/spec/canonicalize.py`
- `tests/spec/test_models.py`
- `tests/spec/test_loader.py`
- `tests/spec/test_hashing.py`
- `tests/fixtures/spec/valid_equivalent.yaml`
- `tests/fixtures/spec/valid_equivalent.json`
- `tests/fixtures/spec/invalid_unknown_field.yaml`
- `docs/ai_handoff/checkpoint_02_report.md`

## Files edited

- `pyproject.toml`: added Pydantic v2 and PyYAML runtime dependencies.
- `.github/workflows/ci.yml`: added the exact Checkpoint 2 specification-test command.
- `qnetbench/__init__.py`: replaced the stale Checkpoint 0 package description.
- `README.md`: updated the current implemented state and development command matrix.
- `PROJECT_STATE.md`: activated Checkpoint 2 and recorded the verification boundary.

## Tests added or changed

- `tests/spec/test_models.py`: proves strict fields, ranges, IDs, references, timing, and unique metrics.
- `tests/spec/test_loader.py`: proves YAML/JSON equivalence, readable errors, unsafe YAML rejection, and malformed input handling.
- `tests/spec/test_hashing.py`: proves canonical equivalence, meaningful-change sensitivity, ordered-list sensitivity, and the golden hash.

## Commands run

Local development environment: CPython 3.13.5. Authoritative Python 3.12 CI is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | 0 | Editable install and dependencies succeeded locally. |
| `python -m ruff check .` | 0 | All local lint checks passed. |
| `python -m ruff format --check .` | 0 | All local formatting checks passed. |
| `python -m pytest -q tests/spec` | 0 | 18 specification tests passed locally. |
| `python -m pytest -q` | pending | Full repository verification pending in GitHub Actions. |
| `git diff --check` | pending | GitHub Actions verification pending. |

## Artifact evidence

- Golden minimal benchmark hash: `fa5b7b457debdb5dde5dd35fea3b5186511ed90cfd350327b5cf7ae837618d97`.
- Equivalent sources: `tests/fixtures/spec/valid_equivalent.yaml` and `tests/fixtures/spec/valid_equivalent.json`.

## Contract and architecture checks

- BenchmarkSpec changed: no; runtime implements frozen v0.1.
- Canonical result contract changed: no.
- `qnetbench.spec` imports adapters, metrics, runners, or simulators: no.
- Unsafe YAML constructors accepted: no.

## Assumptions and decisions

- JSON/YAML arrays normalize to immutable tuples in runtime models and serialize back to JSON arrays.
- Equivalent accepted numeric encodings normalize through typed fields; negative zero normalizes to `0.0`.
- Cross-field errors include the affected contract path in their message when Pydantic cannot assign a nested location.

## Deviations from checkpoint plan

- CI, README, and the package description were updated to remove stale state and make the exact checkpoint gate visible. No future-checkpoint behavior was added.

## Open issues and risks

- Python 3.12 CI verification pending.

## PROJECT_STATE.md update

- Current checkpoint/result: Checkpoint 2 in progress.
- Last passing evidence: local specification checks.
- Next allowed action: complete Checkpoint 2 verification only.

## Final status

STATUS: IN_PROGRESS — Checkpoint 2 verification pending. STOP.
