# Checkpoint 08 Report: Finite sweep, analysis, plots, and mock-pipeline gate

Status: IN_PROGRESS
Date (UTC): 2026-07-20
Branch: `checkpoint-08-mock-pipeline`
Commit: pending CI-verified head
Previous good commit: `8d872c8ba3c8bdae84c52755c160e139260cc5c8`
Active contract versions: benchmark 0.1 frozen; result 0.1 frozen; metrics 0.1 frozen

## Scope under verification

- Strict separate SweepSpec v0.1 with approved finite scalar axes and explicit seeds.
- Deterministic lexical-axis cartesian expansion with a hard 100-run preflight cap.
- Sequential delegation to the existing single-run pipeline.
- Stable sweep manifest, child bundles, deterministic aggregate CSV, and exactly
  two approved plots.
- Full mock-pipeline gate across all four frozen benchmarks and the checked-in
  nine-run sweep.
- No SeQUeNCe research, simulator adapter, parallelism, resume, retry, database,
  dashboard, or frozen-contract change.

## Checked-in sweep plan

| Run | Loss | Seed | Benchmark hash | Execution hash |
|---:|---:|---:|---|---|
| 1 | 0.1 | 1 | `01b79a942b6742b1f53ada9bcaf12622af82e3eca835a2ef1fab6fe7ece92a25` | `361ed58c3260d8e9fd401024dad1becdc7c2a834463e66d3a5b1b8ef68aba1f4` |
| 2 | 0.1 | 2 | `01b79a942b6742b1f53ada9bcaf12622af82e3eca835a2ef1fab6fe7ece92a25` | `c03a594a37edf5ccfa94b664cdb2fa1a25b0f9396c710742cf42a7964d058051` |
| 3 | 0.1 | 3 | `01b79a942b6742b1f53ada9bcaf12622af82e3eca835a2ef1fab6fe7ece92a25` | `3a43f5107fa08bc8fbdb1241ebc1fc0be230f8dc6065a0d5697f9fe68e8e9fa4` |
| 4 | 0.2 | 1 | `3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf` | `fb8cdcf0157ab3e943d22f6dd8654008e4f1f9ce6b2337411420f51e87272c60` |
| 5 | 0.2 | 2 | `3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf` | `202bf5fc20daaebc66b8ede018f18fef9e3fcab85395c0d72062187fa2eb6d81` |
| 6 | 0.2 | 3 | `3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf` | `161e749e23a642aa0145e244ede10558408327105a4b120553935534c10a1984` |
| 7 | 0.3 | 1 | `884eae5f45052e19e373b6e4dda1466c17ddb0fe2fc1855ea7186dc4d379d98a` | `3f7d9e29ab2d6c6c0e0a78e05f69240a56d57c90b8b7f6b3bc318d0d83997b7a` |
| 8 | 0.3 | 2 | `884eae5f45052e19e373b6e4dda1466c17ddb0fe2fc1855ea7186dc4d379d98a` | `66386b6b6ce20237477c179e62c5bcf373df3ca81647cb1d014b567b0933d2e4` |
| 9 | 0.3 | 3 | `884eae5f45052e19e373b6e4dda1466c17ddb0fe2fc1855ea7186dc4d379d98a` | `71c7adb7910f7c6878da3cb80c9482859d7db8824fa20626579f2c11ff28c9b5` |

## Aggregate columns

`parameters_json`, `metric_id`, `unit`, `n_runs`, `n_ok`, `mean`,
`sample_std`, `minimum`, `maximum`.

## Approved plot filenames

- `request_success_probability.png`
- `latency_mean_s.png`

## Verification status

Authoritative clean Python 3.12 CI and artifact evidence are pending. The
`mock_pipeline_ready` flag remains false until the exact final head passes.

## Final status

STATUS: IN_PROGRESS — Checkpoint 8 verification pending. STOP.
