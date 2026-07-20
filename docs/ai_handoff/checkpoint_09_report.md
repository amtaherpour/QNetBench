# Checkpoint 09 Report: Verified backend research and semantic mapping freeze

Status: IN_PROGRESS
Date (UTC): 2026-07-20
Branch: `checkpoint-09-semantic-mapping`
Previous good commit: `ac0479fe1cfa954cc59f743918b10fca7e834512`

## Goal

Remove simulator API, unit, seed, timing, fidelity, request, status, attempts,
path, and raw-extraction uncertainty before production adapter code.

## Required targets

- SeQUeNCe 1.0.0 at commit `ffd7c837f932c7bdc9450cd211aaf75b4d6a99a5`.
- Q2NS commit `f22ba28f437099ba3cf9956ca332ba5ce8bb14fd` on
  ns-3.47 commit `e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f`.
- QuISP qualification decision at commit
  `2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c`.
- NetSquid optional BYO/private-CI boundary without fabricated credentials.

## Verified evidence so far

- SeQUeNCe link-2 and chain-3 mapping passed in workflow 29715128630.
- Same-seed records were identical, alternate-seed evidence was recorded, and a
  detector-disabled controlled failure produced zero successful requests.
- The successful SeQUeNCe artifact is 8450288447 with digest
  `sha256:407dcecefce15682e165100eea9afc5ca5083943846bb8171cb522b2d1fe5b4c`.
- The probe uses Barrett-Kok generation with ket-vector formalism, native RSVP
  swapping controls, and a reservation size bounded by intermediate-memory
  requirements.

## Work under final verification

- Q2NS link-2/chain-3 mapping and canonical extraction.
- QuISP headless qualification and promotion decision.
- Accumulated core CI after exact Ruff formatting.
- Final mapping documents, checked-in evidence summaries, conformance tests,
  completion metadata, merge, and independent post-merge audit.

## Scope exclusion

No production adapter, default real-simulator dependency, cross-simulator paper
result, or frozen v0.1 change belongs to this checkpoint.

## Final status

STATUS: IN_PROGRESS — final Checkpoint 9 verification pending.
