# Checkpoint 02 Report: Benchmark loading, normalization, and hashing

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-02-spec-runtime`
Commit: CI-verified head `4258224206e62ad402d673e4fe21cabd452dbfd5`; completion metadata committed afterward
Previous good commit: `37f032009b5b37246d73b9185f7dc50f3c94cc92`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added strict Pydantic v2 models matching BenchmarkSpec v0.1.
- Added safe YAML/JSON loading with typed, path-aware `ConfigError` failures.
- Added deterministic normalized JSON and lowercase SHA-256 hashing.
- Added equivalent-source, strictness, unsafe-YAML, architecture-boundary, and golden-hash tests.
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
- `README.md`: updated the implemented state and development command matrix.
- `PROJECT_STATE.md`: recorded Checkpoint 2 completion and authorized Checkpoint 3 only.

## Tests added or changed

- `tests/spec/test_models.py`: proves strict fields, ranges, IDs, references, timing, unique metrics, numeric-string rejection, and forbidden-import isolation.
- `tests/spec/test_loader.py`: proves YAML/JSON equivalence, readable errors, unsafe YAML rejection, non-finite JSON rejection, and malformed input handling.
- `tests/spec/test_hashing.py`: proves canonical equivalence, meaningful-change sensitivity, ordered-list sensitivity, and the golden hash.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29697121906.

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | 0 | Editable installation and dependencies passed. |
| `python -m ruff check .` | 0 | Lint passed. |
| `python -m ruff format --check .` | 0 | Formatting check passed. |
| `python -m pytest -q tests/contracts` | 0 | Frozen contract tests passed. |
| `python -m pytest -q tests/spec` | 0 | Specification tests passed; 22 passed locally and the same step passed in CI. |
| `python -m pytest -q` | 0 | Full repository test suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

## Artifact evidence

- Golden minimal benchmark hash: `fa5b7b457debdb5dde5dd35fea3b5186511ed90cfd350327b5cf7ae837618d97`.
- Equivalent sources: `tests/fixtures/spec/valid_equivalent.yaml` and `tests/fixtures/spec/valid_equivalent.json`.
- Validation examples include `network.nodes[0].unexpected`, `physical_profile.memory_efficiency`, duplicate node/link IDs, unknown endpoint references, and prohibited top-level `backend`.

## Contract and architecture checks

- BenchmarkSpec changed: no; runtime implements frozen v0.1.
- Canonical result contract changed: no.
- `qnetbench.spec` imports adapters, artifacts, metrics, results, runners, or simulators: no; statically tested.
- Unsafe YAML constructors accepted: no.

## Assumptions and decisions

- JSON/YAML arrays normalize to immutable tuples in runtime models and serialize back to JSON arrays.
- Equivalent accepted numeric encodings normalize through typed fields; negative zero normalizes to `0.0`.
- Cross-field errors include the affected contract path in their message when Pydantic cannot assign a nested location.

## Deviations from checkpoint plan

- CI, README, and the package description were updated to remove stale state and make the exact checkpoint gate visible. No future-checkpoint behavior was added.

## Open issues and risks

- None blocking Checkpoint 3.

## PROJECT_STATE.md update

- Current checkpoint/result: Checkpoint 2 complete.
- Last passing evidence: GitHub Actions CI run 29697121906.
- Next allowed action: Checkpoint 3 only.

## Final status

STATUS: COMPLETE - Checkpoint 2 only. STOP. Next allowed checkpoint: 3.
