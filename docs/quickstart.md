# QNetBench mock quickstart

Install the project in editable mode:

```bash
python -m pip install -e ".[dev]"
```

Inspect the frozen catalog and validate a benchmark:

```bash
qnetbench list
qnetbench validate benchmarks/v0_1/link_2_batch.yaml
```

Run one deterministic synthetic mock execution, then validate and summarize the
saved canonical bundle:

```bash
qnetbench run benchmarks/v0_1/link_2_batch.yaml --backend mock --seed 7 --out results/link-2-seed-7
qnetbench validate-result results/link-2-seed-7
qnetbench summarize results/link-2-seed-7
```

The mock backend is a deterministic contract and pipeline oracle. Its values are
synthetic and must not be interpreted as a physical quantum-network baseline.
Existing output is not replaced unless `--overwrite` is supplied explicitly.
