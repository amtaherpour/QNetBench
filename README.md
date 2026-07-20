# QNetBench

QNetBench is a simulator-neutral benchmark, conformance, and reproducibility layer
for quantum-network simulators. It is **not** a simulator.

## Current status

Checkpoint 8 is complete and independently audited. The core provides frozen
v0.1 benchmark/result/metric contracts, strict benchmark and sweep loading,
canonical bundles, a deterministic synthetic mock oracle, eight standard
metrics, adapter-neutral single-run and finite-sweep orchestration, deterministic
aggregation, two approved plots, seven CLI commands, and four frozen benchmarks.

Checkpoint 8.5 is freezing the paper-track simulator portfolio before production
real adapters are written. The selected open targets are SeQUeNCe and Q2NS;
QuISP is the qualification reserve/possible third backend, and NetSquid is an
optional credentialed bring-your-own-installation reference. A passing research
probe does not yet mean QNetBench supports that backend.

The mock is a contract and pipeline oracle. Its values are synthetic and must
never be interpreted as physical quantum-network results.

## Quick start

```bash
python -m pip install -e ".[dev,plot]"
qnetbench list
qnetbench validate benchmarks/v0_1/link_2_batch.yaml
qnetbench run benchmarks/v0_1/link_2_batch.yaml --backend mock --seed 7 --out results/link-2-seed-7
qnetbench validate-result results/link-2-seed-7
qnetbench summarize results/link-2-seed-7
qnetbench sweep sweeps/v0_1/link_loss_small.yaml --backend mock --out results/link-loss-small
qnetbench plot results/link-loss-small
```

Existing single-run output is replaced only with explicit `--overwrite`. Existing
sweep output always fails; alpha has no resume, retry, parallel, or sweep-overwrite
mode.

## Paper track

After Checkpoint 8.5 the finite roadmap is: executable semantic mapping freeze,
production conforming open adapters, cross-simulator scientific validation and
reference corpus, then the independently audited paper-ready public release.
Details are in `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`, with ADRs
under `docs/decisions/` and evidence under `docs/research/` and `simulators/`.

## Frozen catalog

| File | Benchmark ID | Nodes | Links |
|---|---|---:|---:|
| `link_2_batch.yaml` | `qnb-v0-1-link-2-batch` | 2 | 1 |
| `chain_3_batch.yaml` | `qnb-v0-1-chain-3-batch` | 3 | 2 |
| `chain_5_batch.yaml` | `qnb-v0-1-chain-5-batch` | 5 | 4 |
| `grid_3x3_batch.yaml` | `qnb-v0-1-grid-3x3-batch` | 9 | 12 |

Hashes and frozen scientific values are recorded in
`benchmarks/v0_1/README.md`.

## Development checks

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
```

Read `AGENTS.md`, `PROJECT_STATE.md`, and the documents under `docs/planning/`
before changing checkpoint-controlled behavior.

## License

BSD-3-Clause. See `LICENSE`.
