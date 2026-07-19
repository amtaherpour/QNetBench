# Metric Definitions v0.1

Every CSV row has stable columns: `metric_id,status,value,unit,population_count,coverage_count`. Status is `ok`, `unavailable`, or `not_applicable`; non-ok rows have a blank value and never NaN or infinity.

| Metric ID | Definition | Population |
|---|---|---|
| `request_success_probability` | successes / planned requests | all planned requests |
| `latency_mean_s` | arithmetic mean latency | successful requests |
| `latency_median_s` | median latency | successful requests |
| `latency_p95_s` | nearest-rank p95 | successful requests |
| `fidelity_mean` | arithmetic mean fidelity | successful requests; complete coverage required |
| `fidelity_median` | median fidelity | successful requests; complete coverage required |
| `throughput_success_per_s` | successes / measurement duration | manifest measurement window |
| `attempts_per_success` | sum known attempts / successes | complete attempt coverage required |

Zero-success latency and fidelity rows are unavailable, not zero. Nearest-rank p95 uses index `ceil(0.95*n)-1`. Metrics read only `run_manifest.json` and `requests.jsonl`.
