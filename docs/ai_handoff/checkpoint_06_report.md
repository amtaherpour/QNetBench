# Checkpoint 06 Report: Single-run orchestration and CLI

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-06-runner-cli`
Commit: CI-verified implementation head `3f3008700ea9df06a2532d16a2f53ffc9767a777`; completion metadata committed afterward
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
- `PROJECT_STATE.md`: recorded completion and authorized Checkpoint 7 only.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29700289691.

| Command | Exit | Result |
|---|---:|---|
| editable development install | 0 | Typer and console script installed. |
| `python -m ruff check .` | 0 | Lint passed. |
| `python -m ruff format --check .` | 0 | Formatting passed. |
| accumulated focused suites through metrics | 0 | All prior checkpoint tests passed. |
| `python -m pytest -q tests/runners tests/cli` | 0 | Runner and CLI tests passed. |
| installed `qnetbench` help/validate/run/validate-result/summarize smoke | 0 | Complete mock bundle created, read, summarized, and revalidated. |
| `python -m pytest -q` | 0 | Full repository suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

## Failure-path evidence

- Unsupported benchmark: failed bundle with stage `support_check`, no standard metrics, nonzero caller result.
- Synthetic adapter exception: failed bundle with stage `execution`, sanitized traceback, nonzero CLI exit.
- Existing output: rejected before execution unless `--overwrite` is explicit.
- Corrupted benchmark hash: `validate-result` returns nonzero and identifies the hash mismatch.

## Architecture checks

- Runner imports no concrete mock or real adapter module.
- CLI delegates to the runner and bundle reader rather than duplicating scientific logic.
- `summarize` reads validated saved metric rows and never re-executes a backend.

## Quality note

The first branch CI run exposed an incorrect expected field name in one negative CLI assertion. The assertion was corrected to the actual frozen fixture field (`backend`), and the entire accumulated Python 3.12 gate then passed. Only the passing final implementation head is accepted as evidence.

## Open issues and risks

- None blocking Checkpoint 7.

## Final status

STATUS: COMPLETE - Checkpoint 6 only. STOP. Next allowed checkpoint: 7.
