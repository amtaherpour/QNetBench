# ADR-0001: Freeze v0.1 Contract Boundaries

Status: Accepted

## Decision

`BenchmarkSpec` contains only backend-independent scientific input. Backend, seed, output path, overwrite policy, and sweeps belong to separate execution requests. Canonical run manifests and terminal request records are the only standard metric inputs. JSON Schemas and contract documents are normative; examples are informative unless designated fixtures.

## Consequences

Adapters translate validated specifications but do not calculate standard metrics or own final bundle layout. Metrics cannot import adapters or read raw backend output. After Checkpoint 1, a breaking contract change requires explicit human approval, an ADR, fixture updates, and a schema-version or approved pre-release migration decision.
