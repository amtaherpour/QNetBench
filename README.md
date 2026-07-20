# QNetBench

QNetBench is a simulator-neutral benchmark, conformance, and reproducibility layer
for quantum-network simulators. It is **not** a simulator.

## Current status

Checkpoint 8.5 is complete subject to the final merge/audit. The independently
audited mock pipeline provides frozen v0.1 contracts, canonical artifacts,
standard metrics, single runs, bounded sweeps, deterministic aggregation, and
approved plots. The paper-track simulator portfolio is now frozen:

- mandatory open targets: SeQUeNCe and Q2NS;
- qualification reserve/possible third backend: QuISP;
- optional credentialed BYO reference: NetSquid;
- deterministic non-physical software oracle: mock.

The public probes qualify these research targets but do not yet make them
QNetBench-supported backends. Exact semantic mappings are frozen in Checkpoint 9,
and production adapters begin only in Checkpoint 10.

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

The finite roadmap is: Checkpoint 9 executable semantic mapping freeze,
Checkpoint 10 production conforming open adapters, Checkpoint 11 cross-simulator
scientific validation/reference corpus, and Checkpoint 12 paper-ready public
release. See `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`.

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
