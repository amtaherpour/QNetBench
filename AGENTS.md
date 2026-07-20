# AGENTS.md — QNetBench

## Mission

QNetBench is a simulator-neutral benchmark, conformance, and reproducibility
layer for quantum-network simulators. It is not a simulator. The paper-track goal
is an openly reproducible multi-simulator standard whose claims are traceable to
validated canonical artifacts.

## Read before editing

1. `PROJECT_STATE.md`
2. Versioned contracts under `docs/contracts/` and `schemas/`
3. `docs/planning/QNetBench_Improved_AI_Handoff_Manual_v0_2.md`
4. `docs/planning/QNetBench_Codex_Execution_Control_Plan_v0_1.md`
5. `docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md`
6. Relevant files under `docs/decisions/`, `docs/research/`, and `simulators/`
7. The latest checkpoint and independent-audit reports

The original control plan is historical authority for completed Checkpoints 0–8.
The paper-track roadmap is authoritative from Checkpoint 8.5 onward.

## Work control

- Work on exactly one active checkpoint and preserve unrelated human changes.
- Repair every repository-controlled failure before advancing.
- Run every command and external probe required by the active checkpoint.
- Update `PROJECT_STATE.md` and the checkpoint/audit report with exact evidence.
- Do not weaken, delete, skip, or rewrite a test merely to advance.
- Do not claim a command, installation, API, artifact, or simulator behavior was
  verified unless the recorded environment actually verified it.

## Frozen baseline

Checkpoints 0–8 are complete and independently audited. Without a separately
versioned ADR and migration plan, do not change:

- BenchmarkSpec, canonical-result, or metric contracts v0.1;
- files under `schemas/v0_1/` or `docs/contracts/`;
- the four frozen benchmark files, IDs, scientific values, or hashes;
- standard metric semantics or canonical bundle invariants;
- the adapter-neutral runner boundary; or
- the deterministic mock algorithm and its non-physical interpretation.

## Architectural invariants

- Backend, seed, output, and sweep settings are execution concerns, not benchmark
  fields.
- Canonical request records and the run manifest are the only metric inputs.
- Metrics never import adapters or read simulator/raw output.
- Simulator APIs stay in `qnetbench/adapters/<name>.py`, an approved bridge, or a
  checkpoint-controlled research probe.
- Adapters emit canonical records in memory, never compute metrics, and never
  write final bundles.
- Unsupported fields are reported explicitly; there is no silent coercion,
  fallback, guessed default, or fabricated observable.
- Mock output is synthetic and can never be cited as physical evidence.
- Numeric equality across independent real simulators is not required; semantic
  conformance, pinned provenance, and common metrics are required.

## Paper-track portfolio

- Required open targets: SeQUeNCe and Q2NS, subject to Checkpoint 9 executable
  semantic conformance.
- Qualification reserve/possible third target: QuISP.
- Optional credentialed reference: NetSquid as a bring-your-own-installation
  plugin/private-CI lane; it never blocks the open core.
- Do not create production real-simulator adapters before Checkpoint 9 freezes
  exact mappings and conformance fixtures.
- Default CI must not install any real simulator.

## Current finite roadmap

- Checkpoint 9: verified backend micro-scenarios and semantic mapping freeze.
- Checkpoint 10: production conforming open adapters.
- Checkpoint 11: cross-simulator scientific validation and reference corpus.
- Checkpoint 12: paper-ready public release and independent reproduction audit.

Do not create further top-level checkpoints without explicit human approval and
an ADR.

## Standard commands

```bash
python -m pip install -e ".[dev,plot]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
```

Use checkpoint-specific workflows for isolated real-simulator research.

## External constraints

A repository-controlled problem must be solved. A genuine external constraint
such as private credentials or a third-party license is documented with exact
evidence and isolated to its optional lane while all open work continues. Never
fabricate access, accept terms for the user, store credentials, or represent a
source-only probe as runtime conformance.

## Publishing

Do not force-push, tag, publish packages, create a GitHub release, mint a DOI,
submit a paper, or make external scientific claims without explicit human
authorization.
