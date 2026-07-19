# Checkpoint 06 Report: Single-run orchestration and CLI

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-06-runner-cli`
Commit: pending CI-verified head
Previous good commit: `185a8134f3f33ac22ec918b2bc4b150cf48e5be9`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added adapter-neutral single-run orchestration and execution provenance hashing.
- Added readable run IDs derived from explicit provenance rather than used as provenance.
- Added complete and failed bundle paths through the existing atomic writer.
- Added Typer CLI commands `validate`, `run`, `summarize`, and `validate-result`.
- Added installed-entrypoint smoke commands and positive, corruption, overwrite, support-failure, and execution-failure tests.
- Added no benchmark catalog/list command, sweep, plot, or SeQUeNCe behavior.

## Execution identity

The execution SHA-256 includes normalized benchmark hash, adapter name/version, backend name/version, seed, and an explicit empty execution-options object. It excludes timestamps, run ID, output path, and machine-specific values. The readable run ID is `<benchmark-id>-<backend>-<seed>-<execution-hash-prefix>`.

## Files created

- `qnetbench/runners/__init__.py`
- `qnetbench/runners/single.py`
- `qnetbench/cli.py`
- `tests/runners/`
- `tests/cli/`
- `docs/ai_handoff/checkpoint_06_report.md`

## Files edited

- `qnetbench/errors.py`: added `RunError` carrying the failed-bundle path.
- `pyproject.toml`: added Typer and the `qnetbench` console script.
- `.github/workflows/ci.yml`: added exact runner/CLI tests and installed-command smoke.
- `PROJECT_STATE.md`: activated Checkpoint 6 and its verification boundary.

## Commands run

Authoritative Python 3.12 CI verification is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m ruff check qnetbench/runners qnetbench/cli.py qnetbench/errors.py tests/runners tests/cli` | 0 | Focused lint passed locally. |
| `python -m ruff format --check qnetbench/runners qnetbench/cli.py qnetbench/errors.py tests/runners tests/cli` | 0 | Focused formatting passed locally. |
| `python -m pytest -q tests/runners tests/cli` | 0 | 13 focused tests passed locally. |
| `python -m qnetbench.cli --help` | 0 | Exactly the four Checkpoint 6 commands were exposed. |
| module CLI validate/run/validate-result/summarize smoke | 0 | Complete mock bundle was created and revalidated. |
| `python -m pytest -q` | pending | Python 3.12 CI pending. |
| `git diff --check` | pending | Python 3.12 CI pending. |

## Failure-path evidence

- Unsupported benchmark: failed bundle with stage `support_check`, no standard metrics, nonzero caller result.
- Synthetic adapter exception: failed bundle with stage `execution`, sanitized traceback, nonzero CLI exit.
- Existing output: rejected before execution unless `--overwrite` is explicit.
- Corrupted benchmark hash: `validate-result` returns nonzero and identifies the hash mismatch.

## Architecture checks

- Runner imports no concrete mock or real adapter module.
- CLI delegates to the runner and bundle reader rather than duplicating scientific logic.
- `summarize` reads validated saved metric rows and never re-executes a backend.

## Open issues and risks

- Python 3.12 CI verification pending.

## Final status

STATUS: IN_PROGRESS — Checkpoint 6 verification pending. STOP.
