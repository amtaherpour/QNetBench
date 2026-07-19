# Checkpoint 07 Report: Frozen benchmark catalog and mock documentation

Status: COMPLETE
Date (UTC): 2026-07-19
Branch: `checkpoint-07-catalog`
Commit: CI-verified implementation head `c9163111d65d2b1d945a6a947824fa2594344f27`; completion metadata committed afterward
Previous good commit: `1681918091c79e33b893e22f13316e41fa451e62`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope completed

- Added exactly four static v0.1 alpha benchmarks and recorded their normalized hashes.
- Added stable catalog discovery and the `qnetbench list` command.
- Added catalog, topology, hash, mock-run, list, architecture, and documentation-smoke tests.
- Added quickstart, adapter, reproducibility, support-matrix, catalog, and README documentation.
- Added no generator API, sweep, plot, or SeQUeNCe behavior.

## Frozen catalog

| File | Benchmark ID | Requests | Hash |
|---|---|---:|---|
| `link_2_batch.yaml` | `qnb-v0-1-link-2-batch` | 16 | `3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf` |
| `chain_3_batch.yaml` | `qnb-v0-1-chain-3-batch` | 16 | `8f44be6e6310fda341a7efeb5921dfadd90cff76196b1efb3aa7c076447ac13b` |
| `chain_5_batch.yaml` | `qnb-v0-1-chain-5-batch` | 16 | `caf650aeb6f0a396ba65043b10c9f2bd2f56989e53e3b15d553adbc0aa86dc93` |
| `grid_3x3_batch.yaml` | `qnb-v0-1-grid-3x3-batch` | 16 | `4b982542ea2fe6ae094c764acb89fb16dc9ecd8cb78835f33b46f33179649900` |

All four use empty `extensions`, fixed batch arrivals, deterministic shortest-path routing, no purification, and all eight standard metrics. The grid's lexical equal-length route is `n00,n01,n02,n12,n22`; it and both multi-hop chains use sequential swapping.

## Development smoke durations

Measured in the development environment using seed 1 and fresh temporary output directories:

| Benchmark | Seconds |
|---|---:|
| link_2_batch | 0.017707 |
| chain_3_batch | 0.008749 |
| chain_5_batch | 0.008974 |
| grid_3x3_batch | 0.014102 |

These are operational smoke durations, not benchmark metrics or performance claims.

## Commands run

Authoritative environment: GitHub-hosted Ubuntu 24.04 with CPython 3.12, CI run 29700632114.

| Command | Exit | Result |
|---|---:|---|
| editable development install | 0 | Project and console script installed. |
| `python -m ruff check .` | 0 | Lint passed. |
| `python -m ruff format --check .` | 0 | Formatting passed. |
| accumulated focused suites through runner/CLI | 0 | All prior checkpoint tests passed. |
| `python -m pytest -q tests/catalog tests/cli/test_list.py` | 0 | Catalog and stable-list tests passed. |
| `qnetbench list` | 0 | Exactly four catalog entries printed in stable order. |
| four catalog validate/run/validate-result/summarize command sequences | 0 | All four mock bundles completed and revalidated. |
| `python -m pytest -q` | 0 | Full repository suite passed. |
| `git diff --check` | 0 | Whitespace check passed. |

## Architecture and support checks

- `qnetbench.catalog` imports no adapters or simulator packages.
- The mock supports all four catalog cases and remains explicitly synthetic.
- Support matrix marks every SeQUeNCe case `not started`.
- No backend-specific extension appears in a frozen benchmark.
- Exactly four `.yaml` benchmark files exist in `benchmarks/v0_1/`.

## Open issues and risks

- None blocking the cumulative post-Checkpoint-7 audit.
- `mock_pipeline_ready` remains false because Checkpoint 8 has not run.

## Final status

STATUS: COMPLETE - Checkpoint 7 only. STOP. Next allowed action: cumulative audit through Checkpoint 7.
