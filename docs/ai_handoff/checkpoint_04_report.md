# Checkpoint 04 Report: Adapter interface, registry, and deterministic mock adapter

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-04-mock-adapter`
Commit: pending CI-verified head
Previous good commit: `ee714b0093d9dff17a941d500af3abb39e66af3e`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added the adapter ABC, backend identity, support report, and in-memory adapter-run boundary.
- Added a deterministic adapter registry with the mock backend registered by name.
- Added synthetic deterministic shortest-path mock execution for the complete alpha feature subset.
- Added golden records, alternate-seed checks, canonical-record tests, support rejection, and architecture-boundary tests.
- Added no metric computation, bundle writing, real simulator dependency, or SeQUeNCe adapter.

## Mock algorithm

- Version: `1.0`.
- Random inputs: mock algorithm version, normalized benchmark SHA-256, explicit integer seed, request ID, and draw label.
- Random primitive: the first 64 bits of SHA-256; wall-clock time, global random state, process ID, output path, and file order are excluded.
- Routing: weighted shortest path by `length_km`, with the full node-ID tuple as the lexical tie-break.
- Output is explicitly labeled synthetic and is not a physical model or physics baseline.

## Files created

- `qnetbench/adapters/__init__.py`
- `qnetbench/adapters/base.py`
- `qnetbench/adapters/registry.py`
- `qnetbench/adapters/mock.py`
- `tests/adapters/test_support_report.py`
- `tests/adapters/test_mock_determinism.py`
- `tests/adapters/test_mock_records.py`
- `tests/fixtures/mock/golden_seed_1.jsonl`
- `docs/ai_handoff/checkpoint_04_report.md`

## Files edited

- `qnetbench/errors.py`: added typed adapter and unsupported-benchmark errors.
- `.github/workflows/ci.yml`: added the exact Checkpoint 4 adapter test command.
- `PROJECT_STATE.md`: activated the Checkpoint 4 verification boundary.

## Commands run

Authoritative Python 3.12 GitHub Actions verification is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m ruff check qnetbench/adapters qnetbench/errors.py tests/adapters` | 0 | Development lint passed. |
| `python -m ruff format --check qnetbench/adapters qnetbench/errors.py tests/adapters` | 0 | Development formatting passed. |
| `python -m pytest -q tests/adapters` | 0 | 10 adapter tests passed in development. |
| `python -m pytest -q` | pending | Python 3.12 CI pending. |
| `git diff --check` | pending | Python 3.12 CI pending. |

## Support report evidence

Supported minimal benchmark: `supported=true`, no unsupported paths, warning that mock output is synthetic.

Unsupported direct-link fixture with sequential swapping: `supported=false`, path `protocol.swapping`, reason that a two-node path requires `none`.

## Open issues and risks

- Python 3.12 CI verification pending.

## Final status

STATUS: IN_PROGRESS — Checkpoint 4 verification pending. STOP.
