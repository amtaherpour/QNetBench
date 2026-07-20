# QNetBench mock quickstart

Install the project with the approved plotting extra:

```bash
python -m pip install -e ".[dev,plot]"
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

Run the checked-in bounded nine-run sweep and create only the approved plots:

```bash
qnetbench sweep sweeps/v0_1/link_loss_small.yaml --backend mock --out results/link-loss-small
qnetbench plot results/link-loss-small
```

The sweep writes `sweep_manifest.json`, nine canonical child bundles,
`aggregate_metrics.csv`, `plots/request_success_probability.png`, and
`plots/latency_mean_s.png`. It executes sequentially and has no resume, retry,
parallelism, or implicit overwrite behavior.

The mock backend is a deterministic contract and pipeline oracle. Its values are
synthetic and must not be interpreted as a physical quantum-network baseline.
Existing single-run output is not replaced unless `--overwrite` is supplied
explicitly; existing sweep output always fails.
