# Checkpoint 05 Report: Backend-independent metric engine

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-05-metrics`
Commit: CI-verified implementation head `5714cd3a3abcb88a54e2944665bcca2c88c8df9a`; completion metadata committed afterward
Previous good commit: `feaf0a424c30fb3eb2631bfc138da02fb2b1e678`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added the frozen eight-metric registry with stable units and populations.
- Added pure calculations over a complete canonical run manifest and request records.
- Added exact unavailable behavior, coverage counts, nearest-rank p95, and duration validation.
- Added hand-calculated positive and edge-case fixtures plus architecture-boundary tests.
- Added no runner, CLI, plotting, sweep, adapter-specific metric, or contract change.

## Files created

- `qnetbench/metrics/__init__.py`
- `qnetbench/metrics/models.py`
- `qnetbench/metrics/definitions.py`
- `qnetbench/metrics/compute.py`
- `tests/metrics/`
- `docs/ai_handoff/checkpoint_05_report.md`

## Files edited

- `qnetbench/errors.py`: added `MetricComputationError`.
- `.github/workflows/ci.yml`: added the exact Checkpoint 5 metric test command.
- `PROJECT_STATE.md`: recorded completion and authorized Checkpoint 6 only.

## Fixture expectations

| Metric | Fixture expectation | Status | Population | Coverage |
|---|---:|---|---:|---:|
| request_success_probability | 3 / 4 = 0.75 | ok | 4 | 4 |
| latency_mean_s | 2.0 | ok | 3 | 3 |
| latency_median_s | 2.0 | ok | 3 | 3 |
| latency_p95_s | 3.0 nearest-rank | ok | 3 | 3 |
| fidelity_mean | 0.9 | ok | 2 | 2 |
| fidelity_median | 0.9 | ok | 2 | 2 |
| throughput_success_per_s | 1 / 4 = 0.25 | ok | 1 | 1 |
| attempts_per_success | (1 + 3) / 1 = 4.0 | ok | 2 | 2 |

Zero-success latency, fidelity, and attempts rows are unavailable. Partial fidelity or attempt coverage is unavailable rather than averaged selectively. Zero or negative measurement duration makes throughput unavailable.

## Architecture boundary

An AST-based test scans every `qnetbench/metrics/*.py` import and rejects adapters, artifacts, simulator packages, or SeQUeNCe imports.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29699911257.

| Command | Exit | Result |
|---|---:|---|
| `python -m pip install -e ".[dev]"` | 0 | Editable installation passed. |
| `python -m ruff check .` | 0 | Lint passed. |
| `python -m ruff format --check .` | 0 | Formatting passed after one test-layout correction. |
| `python -m pytest -q tests/contracts` | 0 | Frozen contract tests passed. |
| `python -m pytest -q tests/spec` | 0 | Specification tests passed. |
| `python -m pytest -q tests/results tests/artifacts` | 0 | Result and artifact tests passed. |
| `python -m pytest -q tests/adapters` | 0 | Adapter tests passed. |
| `python -m pytest -q tests/metrics` | 0 | Fourteen metric tests passed. |
| `python -m pytest -q` | 0 | Full repository suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

## Quality note

The first branch CI attempt passed lint but identified one file that did not match Ruff's formatter. The file was formatted and the complete accumulated Python 3.12 gate then passed. Only the passing final implementation head is accepted as evidence.

## Open issues and risks

- None blocking Checkpoint 6.

## Final status

STATUS: COMPLETE - Checkpoint 5 only. STOP. Next allowed checkpoint: 6.
