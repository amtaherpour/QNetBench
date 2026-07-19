# Canonical Result Contract v0.1

A complete run directory contains `benchmark.yaml`, `run_manifest.json`, `requests.jsonl`, `metrics.csv`, and `summary.json`. Optional `events.jsonl` and `raw/` are never metric inputs. A failed run contains a failed `run_manifest.json` and `error.json` and does not produce standard metrics.

Every complete run has exactly one terminal request record per planned request. Request IDs are unique. Terminal time is not earlier than submission time, and latency equals their difference within tolerance. Status is one of `success`, `failed`, `timed_out`, or `rejected`. Unavailable fidelity, attempts, and path values are `null`, never guessed.

The manifest records hashes, versions, seed, status, timestamps, measurement window, expected/written counts, environment, warnings, and support digest. `metrics.csv` and `summary.json` are derived from the manifest and request records; `summary.json` is never a metric source.
