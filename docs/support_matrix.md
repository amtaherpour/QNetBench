# Backend support and research matrix

| Benchmark | Mock | SeQUeNCe | Q2NS | QuISP | NetSquid |
|---|---|---|---|---|---|
| `qnb-v0-1-link-2-batch` | supported, synthetic | selected; mapping pending CP9 | selected; mapping pending CP9 | qualification pending CP9 | optional BYO; not probed |
| `qnb-v0-1-chain-3-batch` | supported, synthetic | selected; mapping pending CP9 | selected; mapping pending CP9 | qualification pending CP9 | optional BYO; not probed |
| `qnb-v0-1-chain-5-batch` | supported, synthetic | not in required real-backend profile | not in required real-backend profile | not selected | not selected |
| `qnb-v0-1-grid-3x3-batch` | supported, synthetic | not in required real-backend profile | not in required real-backend profile | not selected | not selected |

“Supported” currently applies only to the deterministic mock software oracle and
is not a claim of physical fidelity. SeQUeNCe and Q2NS passed installation/API or
build/example probes, but they are not QNetBench-supported backends until
Checkpoint 9 freezes exact semantics and Checkpoint 10 implements conforming
production adapters. QuISP has only passed a public-source qualification probe.
NetSquid requires user-specific registration and credentials and remains optional.
