# Mock-pipeline gate

Status: IN_PROGRESS

Checkpoint 8 proves the complete simulator-independent QNetBench pipeline before
any real-simulator research or production adapter begins.

## Gate commands

```bash
python -m pip install -e ".[dev,plot]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/sweeps tests/analysis tests/cli/test_sweep.py
qnetbench sweep sweeps/v0_1/link_loss_small.yaml --backend mock --out .tmp/cp08-sweep
qnetbench plot .tmp/cp08-sweep
python -m pytest -q
git diff --check
```

## Expected checked-in sweep

- sweep ID: `qnb-v0-1-link-loss-small`
- base benchmark: `qnb-v0-1-link-2-batch`
- axis: `physical_profile.fiber_attenuation_db_per_km`
- values: `0.1`, `0.2`, `0.3`
- seeds: `1`, `2`, `3`
- total child runs: `9`
- cap: `100` runs, checked before execution

## Expected artifact layout

```text
<sweep-root>/
  sweep_manifest.json
  aggregate_metrics.csv
  runs/
    001-<execution-hash-prefix>/
    ...
    009-<execution-hash-prefix>/
  plots/
    request_success_probability.png
    latency_mean_s.png
```

Final hashes, aggregate observations, artifact evidence, and the
`mock_pipeline_ready` decision are recorded only after the authoritative Python
3.12 gate passes.
