# QNetBench frozen alpha catalog v0.1

These are the only four alpha benchmark files. Backend, seed, output path, sweep
axes, simulator class names, and extensions are intentionally absent. Scientific
values and normalized SHA-256 hashes are frozen at Checkpoint 7.

| File | Benchmark ID | Requests | Nodes | Links | Normalized SHA-256 |
|---|---|---:|---:|---:|---|
| `link_2_batch.yaml` | `qnb-v0-1-link-2-batch` | 16 | 2 | 1 | `3709721f5f401b33747b69b57c632605070fbba6fe1d40f49ad96dce220f0ecf` |
| `chain_3_batch.yaml` | `qnb-v0-1-chain-3-batch` | 16 | 3 | 2 | `8f44be6e6310fda341a7efeb5921dfadd90cff76196b1efb3aa7c076447ac13b` |
| `chain_5_batch.yaml` | `qnb-v0-1-chain-5-batch` | 16 | 5 | 4 | `caf650aeb6f0a396ba65043b10c9f2bd2f56989e53e3b15d553adbc0aa86dc93` |
| `grid_3x3_batch.yaml` | `qnb-v0-1-grid-3x3-batch` | 16 | 9 | 12 | `4b982542ea2fe6ae094c764acb89fb16dc9ecd8cb78835f33b46f33179649900` |

The grid has multiple equal-length corner-to-corner routes. QNetBench uses the
lexicographically smallest full node-ID path; for `n00` to `n22` this is
`n00,n01,n02,n12,n22`. All cases with intermediate nodes use fixed sequential
swapping. Purification is `none`, routing is deterministic shortest path, and
`extensions` is empty.
