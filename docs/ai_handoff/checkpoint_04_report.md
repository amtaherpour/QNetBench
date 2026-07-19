# Checkpoint 04 Report: Adapter interface, registry, and deterministic mock adapter

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-04-mock-adapter`
Commit: CI-verified implementation head `bf7a4bc175cda21b8a8414d96b9b63153e95c912`; completion metadata committed afterward
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
- `PROJECT_STATE.md`: recorded completion and authorized Checkpoint 5 only.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29699627204.

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | 0 | Editable installation passed. |
| `python -m ruff check .` | 0 | Lint passed after correcting one reported line-length defect. |
| `python -m ruff format --check .` | 0 | Formatting passed. |
| `python -m pytest -q tests/contracts` | 0 | Frozen contract tests passed. |
| `python -m pytest -q tests/spec` | 0 | Specification tests passed. |
| `python -m pytest -q tests/results tests/artifacts` | 0 | Result and artifact tests passed. |
| `python -m pytest -q tests/adapters` | 0 | Adapter tests passed. |
| `python -m pytest -q` | 0 | Full repository test suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

## Support report evidence

Supported minimal benchmark: `supported=true`, no unsupported paths, warning that mock output is synthetic.

Unsupported direct-link fixture with sequential swapping: `supported=false`, path `protocol.swapping`, reason that a two-node path requires `none`.

## Quality note

The first branch CI attempt failed at Ruff because one source line exceeded the repository's configured length. The line was corrected; the subsequent full Python 3.12 gate passed every step. Only the passing final implementation head is accepted as Checkpoint 4 evidence.

## Open issues and risks

- None blocking Checkpoint 5.

## Final status

STATUS: COMPLETE - Checkpoint 4 only. STOP. Next allowed checkpoint: 5.
