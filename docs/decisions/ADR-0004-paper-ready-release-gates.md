# ADR-0004: Paper-ready roadmap and release gates

- Status: accepted
- Date: 2026-07-20
- Supersedes: original Checkpoints 9–11 after the completed Checkpoint 8 gate

## Context

The original roadmap ended with one narrow SeQUeNCe alpha adapter and packaging.
The project goal is now a durable multi-simulator benchmark standard with a
strong public paper, reference artifacts, and an adoption path. The roadmap must
remain finite and checkpoint-gated rather than expanding without an endpoint.

## Decision

Use four remaining top-level checkpoints:

### Checkpoint 9 — Verified backend research and semantic mapping freeze

- create executable link-2 and chain-3 micro-scenarios for SeQUeNCe and Q2NS;
- pin versions/revisions, licenses, installation recipes, seeds, units, and raw
  extraction points;
- qualify QuISP headless execution and decide whether to promote it;
- define the NetSquid BYO plugin boundary and run a credentialed probe only when
  authorized credentials are available;
- freeze conformance fixtures and mapping documents before production adapters.

### Checkpoint 10 — Production open multi-simulator adapters

- implement SeQUeNCe and Q2NS adapters behind the existing boundary;
- use separate sub-gates for each adapter while keeping one top-level checkpoint;
- implement QuISP only if Checkpoint 9 promotes it;
- keep NetSquid optional and separately installed;
- require canonical bundles, deterministic/repeatability evidence, support
  reports, controlled failures, and the full accumulated regression suite.

### Checkpoint 11 — Cross-simulator scientific validation and reference corpus

- run matched frozen scenarios and seeds across all conforming backends;
- publish canonical reference bundles, provenance, semantic-difference tables,
  coverage/unavailable analysis, and reproducible paper figures/tables;
- validate that conclusions do not depend on mock output or hidden defaults;
- do not require numerical equality between simulators.

### Checkpoint 12 — Paper-ready public release

- release-quality package, documentation, examples, contribution/governance
  policy, conformance kit, changelog, citation metadata, and artifact capsule;
- archive reference data and software with persistent identifiers after explicit
  human publication authorization;
- prepare the paper methods, reproducibility, limitations, and artifact appendix;
- independently audit installation and the full release from clean environments.

## Release gates

- No production real adapter before Checkpoint 9 mappings are frozen.
- No cross-simulator claim before at least SeQUeNCe and Q2NS conform.
- QuISP is promoted only by executable evidence.
- NetSquid absence never blocks the open paper core.
- No paper-ready release while `release_candidate_ready` is false.
- Frozen v0.1 contracts remain valid; any v0.2 work is separately versioned.

## Consequences

Only one top-level checkpoint is added beyond the original plan. Checkpoint 12 is
necessary because packaging an alpha and publishing a multi-simulator scientific
artifact are different gates. The project now has a finite, auditable endpoint
rather than an open-ended list of adapters.
