# BenchmarkSpec v0.1

`BenchmarkSpec` describes what is measured, not how a run is executed. It is backend-independent and rejects unknown fields.

Required sections are `schema_version`, `benchmark_id`, `title`, `description`, `network`, `physical_profile`, `workload`, `protocol`, `requested_metrics`, and `extensions`.

Execution concerns are prohibited: `backend`, `seed`, output paths, sweep axes, timeouts, CI settings, and simulator class names. Unit-bearing values use explicit suffixes such as `_s`, `_km`, `_hz`, and `_db_per_km`. IDs are stable and unique within scope. Non-finite numbers are invalid. Frozen alpha benchmarks use an empty `extensions` object.

The normative machine-readable definition is `schemas/v0_1/benchmark.schema.json`. Cross-field invariants include unique node/link IDs, link endpoints that reference nodes, distinct source/destination nodes, and workload nodes that exist in the network.
