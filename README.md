# QNetBench

QNetBench is a Python benchmark and reproducibility layer above quantum-network
simulators. It is **not** a simulator.

## Current status

Checkpoints 0–7 are implemented and verified. The repository provides:

- frozen v0.1 benchmark, result, and metric contracts;
- strict benchmark loading, canonicalization, and SHA-256 hashing;
- canonical complete and failed result bundles with atomic I/O;
- a deterministic synthetic mock adapter;
- the eight backend-independent standard metrics;
- adapter-neutral single-run orchestration;
- a five-command CLI; and
- exactly four frozen v0.1 catalog benchmarks.

The mock backend is a contract and pipeline oracle. Its values are synthetic and
must not be interpreted as physical quantum-network results. SeQUeNCe research
and integration have not started.

## Quick start

```bash
python -m pip install -e ".[dev]"
qnetbench list
qnetbench validate benchmarks/v0_1/link_2_batch.yaml
qnetbench run benchmarks/v0_1/link_2_batch.yaml --backend mock --seed 7 --out results/link-2-seed-7
qnetbench validate-result results/link-2-seed-7
qnetbench summarize results/link-2-seed-7
```

Existing output is never replaced unless `--overwrite` is supplied explicitly.
See `docs/quickstart.md`, `docs/reproducibility.md`, `docs/adapter_guide.md`, and
`docs/support_matrix.md`.

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
