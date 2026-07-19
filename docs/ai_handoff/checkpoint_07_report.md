# Checkpoint 07 Report: Frozen benchmark catalog and mock documentation

Status: IN_PROGRESS
Date (UTC): 2026-07-19
Branch: `checkpoint-07-catalog`
Commit: pending CI-verified head
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

Authoritative Python 3.12 CI verification is pending.

| Command | Exit | Result |
|---|---:|---|
| `python -m ruff check .` | pending | Python 3.12 CI pending. |
| `python -m ruff format --check .` | pending | Python 3.12 CI pending. |
| `python -m pytest -q tests/catalog tests/cli/test_list.py` | pending | Python 3.12 CI pending. |
| `qnetbench list` | pending | Installed-entrypoint CI pending. |
| four catalog `qnetbench run ... --backend mock --seed 1` commands | pending | CI pending. |
| `python -m pytest -q` | pending | Python 3.12 CI pending. |
| `git diff --check` | pending | Python 3.12 CI pending. |

## Architecture and support checks

- `qnetbench.catalog` imports no adapters or simulator packages.
- The mock supports all four catalog cases and remains explicitly synthetic.
- Support matrix marks every SeQUeNCe case `not started`.
- No backend-specific extension appears in a frozen benchmark.

## Open issues and risks

- Python 3.12 CI verification pending.

## Final status

STATUS: IN_PROGRESS — Checkpoint 7 verification pending. STOP.
