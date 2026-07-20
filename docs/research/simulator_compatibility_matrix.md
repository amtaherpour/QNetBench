# Simulator compatibility and risk matrix

Evidence date: 2026-07-20. “Selected” means roadmap selection, not completed
QNetBench adapter conformance.

| Simulator | Portfolio role | Open public CI | Architecture | Seed evidence | Timing/fidelity/request evidence | Primary risk | Decision |
|---|---|---:|---|---|---|---|---|
| Mock | software oracle | yes | QNetBench synthetic Python | deterministic SHA-256 stream | canonical by construction | no physical validity | keep as non-physical oracle |
| SeQUeNCe 1.0.0 | mandatory open backend | yes | native Python discrete-event quantum network | timeline/node seed APIs | documented request app, simulated time, memories, fidelity, throughput | semantic mapping and attempts extraction must be frozen | selected for Checkpoints 9–10 |
| Q2NS v0.1 + ns-3.47 | mandatory open backend | yes | C++ ns-3 classical/quantum co-simulation | `RngSeedManager::SetSeed/SetRun` | ns-3 time, quantum-state backends, nodes/channels, JSON traces | young codebase and QNetBench-specific extraction not yet proven | selected subject to Checkpoint 9 conformance |
| QuISP master / v0.3.0 reference | qualification reserve | source probe only | C++/OMNeT++ repeater-network DES | configuration/seed reproducibility is an explicit project goal | detailed repeater/protocol model, but upstream says swapping data collection is incomplete | OMNeT++ license/build and output extraction | qualify in Checkpoint 9; promote if conformance passes or Q2NS fails |
| NetSquid | optional credentialed reference | no | Python/Cython discrete-event physical components | expected simulator seed controls require credentialed docs/package verification | strong published time/decoherence and state-formalism support | registration, private package index, terms, private CI | BYO plugin; never blocks open core |
| QuNetSim | deferred profile | yes | high-level Python protocol framework | not evaluated for current profile | EPR and application protocols | semantic level differs from v0.1 physical-performance profile | future application benchmark profile |
| SimulaQron/NetQASM | deferred profile | partly | distributed application backend | not evaluated for current profile | application instruction execution | application semantics differ from current profile | future application benchmark profile |
| QKDNetSim | deferred profile | yes | ns-3 QKD/KMS module | ns-3 controls | QKD key generation/management and classical traffic | cannot simulate the frozen entanglement-distribution profile directly | future QKD-specific profile |
| QuNet | deferred profile | yes | Julia cost-vector/routing abstraction | deterministic algorithms possible | abstract accumulated costs/routing | not a direct terminal request record DES | future routing/analytic profile |

## Compatibility conclusions for v0.1

The completed QNetBench core does not need a breaking rewrite. Benchmark files,
canonical request results, manifests, metrics, runner boundaries, and artifact
validation remain simulator-neutral. SeQUeNCe and Q2NS can be researched behind
the existing adapter boundary.

Checkpoint 9 may discover that additional provenance is useful. Such information
must first be recorded in adapter mapping documents or a versioned sidecar. A
breaking field change is permitted only in a separately versioned v0.2 contract,
with migration and compatibility tests; v0.1 files and hashes remain valid.

## Paper comparison policy

QNetBench will not claim that independent simulators should produce identical
numbers. It will require identical benchmark identity, common metric definitions,
explicit semantic mapping, pinned simulator versions, repeatable execution, and
validated canonical artifacts. Differences become research results rather than
hidden adapter behavior.
