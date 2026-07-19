# Reproducibility

QNetBench separates scientific identity from presentation and storage details.

- `benchmark_hash` is SHA-256 over normalized backend-independent benchmark data.
- `execution_hash` includes benchmark hash, adapter/backend identity, seed, and
  explicit execution options; it excludes timestamps and output paths.
- The readable run ID is derived from explicit provenance and is not itself the
  source of truth.
- Canonical request records, manifests, metric rows, and bundle validation are
  backend-independent.
- Existing output is rejected unless overwrite is explicit.

The four v0.1 benchmark files and their hashes are frozen in
`benchmarks/v0_1/README.md`. Mock determinism additionally depends on the recorded
mock algorithm version. Mock outputs are synthetic, so reproducibility does not
imply physical validity.
