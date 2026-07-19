# Checkpoint 05 Report: Backend-independent metric engine

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-05-metrics`
Commit: pending CI-verified head
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
- `PROJECT_STATE.md`: activated Checkpoint 5 and its verification boundary.

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

Authoritative Python 3.12 CI verification is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m ruff check qnetbench/metrics qnetbench/errors.py tests/metrics` | 0 | Focused lint passed locally. |
| `python -m ruff format --check qnetbench/metrics qnetbench/errors.py tests/metrics` | 0 | Focused formatting passed locally. |
| `python -m pytest -q tests/metrics` | 0 | 14 metric tests passed locally. |
| `python -m pytest -q` | pending | Python 3.12 CI pending. |
| `git diff --check` | pending | Python 3.12 CI pending. |

## Open issues and risks

- Python 3.12 CI verification pending.

## Final status

STATUS: IN_PROGRESS — Checkpoint 5 verification pending. STOP.
