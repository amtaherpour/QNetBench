# ADR-0003: Adapter conformance and contract versioning

- Status: accepted
- Date: 2026-07-20

## Context

Adding real simulators can expose differences in terminology, available
observables, timing, fidelity definitions, and seed control. Quietly changing the
frozen v0.1 benchmark or result contracts to fit one simulator would destroy the
cross-simulator standard the project is intended to create.

## Decision

1. `simulators/conformance_v1.yaml` is the required adapter-conformance profile.
2. Every production adapter must pass interface, reproducibility, semantic
   mapping, and paper-backend gates before being used in comparisons.
3. Each mapped input/output is classified as `native`, `derived`, `unavailable`,
   or `unsupported`; derived values require a documented extraction formula.
4. Numerical equality across simulators is not a conformance requirement.
   Benchmark identity, metric semantics, provenance, and artifact validity are.
5. Frozen v0.1 contracts, benchmark files, and hashes remain unchanged.
6. Checkpoint 9 may first record new evidence in mapping documents or a versioned
   sidecar. A breaking field change requires executable evidence, a new ADR, a
   new contract version, migration tooling, and compatibility tests.

## Candidate v0.2 additions

Only if Checkpoint 9 evidence demonstrates need:

- semantic-provenance sidecar for native/derived/unavailable/unsupported values;
- machine-readable capability and support grade;
- raw-event provenance digest and extraction recipe.

These candidates are not implemented or promised by this ADR. They may not alter
v0.1 interpretation.

## Consequences

The existing Checkpoints 0–8 remain valid and reusable for every selected
simulator. Real-adapter complexity stays behind the established adapter boundary.
Paper comparisons can report genuine simulator differences without conflating
them with inconsistent benchmark or metric definitions.
