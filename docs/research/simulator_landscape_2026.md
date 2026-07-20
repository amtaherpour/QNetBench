# Quantum-network simulator landscape — July 2026

Status: research evidence for Checkpoint 8.5. This document selects targets; it
does not claim QNetBench conformance or create production adapters.

## Selection criteria

A paper backend must contribute scientific relevance and a distinct
implementation architecture. It must have a verifiable revision, license,
installation path, seed story, timing model, observable outputs, and a plausible
mapping to the frozen link-2 and chain-3 benchmarks. The openly reproducible core
must not require credentials or proprietary infrastructure.

## Selected mandatory open targets

### SeQUeNCe 1.0.0

Official sources:

- repository: https://github.com/sequence-toolbox/SeQUeNCe
- documentation: https://sequence-rtd-tutorial.readthedocs.io/
- reference paper: https://doi.org/10.1088/2058-9565/ac22f6

SeQUeNCe is an open Python discrete-event simulator with hardware,
entanglement-management, resource-management, network-management, and
application modules. Release 1.0.0 supports Python 3.12 and public pip
installation. The documented topology, request, timeline, seed, fidelity,
memory, and throughput APIs justify full executable mapping research. It is the
primary mature reference backend.

Checkpoint 8.5 installs exactly `sequence==1.0.0`, instantiates and seeds a
timeline, completes an empty kernel run, and inspects the request/topology APIs.
Checkpoint 9 must still prove two-node and three-node scientific mappings and
canonical extraction.

### Q2NS main pinned to an exact commit on ns-3.47

Official sources:

- repository: https://github.com/QuantumInternet-it/q2ns
- software archive: https://doi.org/10.5281/zenodo.19370944
- reference paper: https://doi.org/10.1016/j.comnet.2026.112292

Q2NS is an open C++ quantum-network module built into ns-3. It combines ns-3's
classical discrete-event stack with quantum nodes/channels, selectable ket,
density-matrix, and stabilizer state backends, explicit ns-3 seed/run controls,
and JSON/NDJSON trace support. It provides the strongest architectural contrast
to SeQUeNCe while preserving an open CI path. The current software is young, so
selection is conditional on executable build and conformance evidence rather
than popularity.

The upstream installation instructions currently use the `main` branch rather
than a `v0.1` Git tag. Checkpoint 8.5 therefore records the exact probed Q2NS
commit together with ns-3.47 and runs `q2ns-1-basics-example`. Checkpoint 9 must
create QNetBench-specific link and chain micro-scenarios, prove
timing/fidelity/request extraction, and freeze the trace/mapping recipe.

## Qualification reserve

### QuISP

Official sources:

- repository: https://github.com/sfc-aqua/quisp
- reference paper: https://doi.org/10.1109/ICC.2019.8761588

QuISP is a BSD-licensed C++/OMNeT++ event-driven repeater-network simulator with
large-scale heterogeneous-network ambitions. It is strategically valuable as a
third architecture. However, its own README states that data collection for the
relatively new entanglement-swapping feature is not fully implemented. QuISP also
requires OMNeT++, whose academic use is free but whose licensing differs for
commercial organizations.

Therefore QuISP is not promised as a production paper backend yet. Checkpoint 9
must qualify an exact revision, automated headless installation, seed control,
link/chain request completion, and machine-readable timing/fidelity extraction.
If Q2NS cannot satisfy QNetBench conformance, QuISP is the designated open
fallback without changing v0.1 contracts.

## Optional credentialed reference

### NetSquid

Official sources:

- site and installation: https://netsquid.org/
- reference paper: https://doi.org/10.1038/s42005-021-00647-8

NetSquid is a scientifically influential Python/Cython discrete-event platform
with explicit time/decoherence modeling, multiple quantum-state formalisms, and
modular physical components. It is free to use, but access requires registration,
acceptance of terms, forum credentials, and installation from its private package
index; documentation also requires registration.

NetSquid is therefore a high-value optional bring-your-own-installation plugin
and private-CI lane. It must never block the open SeQUeNCe+Q2NS paper core or
become a dependency of public default CI. Checkpoint 9 may define and test the
plugin boundary without credentials; an actual package probe and comparison
require user-provided authorized credentials and terms-compliant CI.

## Evaluated but deferred profiles

- QuNetSim: useful high-level protocol framework, but not the initial frozen
  physical-performance request profile.
- SimulaQron/NetQASM: valuable application execution environment, but its primary
  semantics differ from QNetBench's current physical request/result profile.
- QKDNetSim: strong QKD key-management and classical-network simulator; it should
  be addressed by a future QKD-specific benchmark profile rather than forced into
  the entanglement-distribution v0.1 contract.
- QuNet: scalable Julia cost-vector and routing abstraction, but not a direct
  discrete-event canonical request-result match.

## Portfolio decision

The open paper core targets SeQUeNCe and Q2NS. QuISP remains the qualified
reserve/possible third backend. NetSquid remains the optional credentialed
reference. The mock remains only a deterministic software oracle.

This portfolio spans native Python simulation and ns-3 classical/quantum
co-simulation, with an OMNeT++ reserve and an influential credentialed reference.
Numeric equality across simulators is not expected; semantic conformance,
reproducibility, and explicit differences are required.
