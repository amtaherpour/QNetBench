# AGENTS.md — QNetBench

## Mission

QNetBench is a benchmark and reproducibility layer above quantum-network simulators. It is not a simulator.

## Read before editing

1. `PROJECT_STATE.md`
2. Versioned contracts under `docs/contracts/` and `schemas/` when they exist
3. `docs/planning/QNetBench_Improved_AI_Handoff_Manual_v0_2.md`
4. `docs/planning/QNetBench_Codex_Execution_Control_Plan_v0_1.md`
5. The latest `docs/ai_handoff/checkpoint_*_report.md`
6. Open blocker reports and relevant ADRs when they exist

## Work control

- Work on exactly one active checkpoint.
- Preserve unrelated human changes.
- Run every command required by the active checkpoint.
- Update `PROJECT_STATE.md` and write a checkpoint or blocker report.
- Stop after reporting. Do not start the next checkpoint without a new instruction.

## Architectural invariants

- `BenchmarkSpec` is backend-independent. Backend, seed, output, and sweeps are execution concerns.
- Canonical request records and the run manifest are the only metric inputs.
- Metrics must never import adapters or read raw backend output.
- Simulator-specific imports and API calls stay in `qnetbench/adapters/<name>.py` or an approved research tool.
- Adapters report unsupported fields explicitly; there is no silent coercion or fallback.
- The deterministic mock adapter must complete end to end before SeQUeNCe production work.
- Do not create `qnetbench/adapters/sequence.py` before Checkpoint 10.
- Do not change frozen contracts, hashes, benchmark values, or metric semantics without explicit approval and an ADR/version decision.

## Alpha scope

- Target release: `0.1.0a1` after Checkpoint 11.
- Required backends: deterministic mock; SeQUeNCe for link-2 and chain-3 only.
- Required catalog: link-2, chain-3, chain-5, and grid-3x3.
- Out of scope: additional simulators, purification, random or adaptive routing, dynamic arrivals, generalized resource metrics, parallel or resumable sweeps, dashboards, paper publication, DOI creation, and additional adapters.

## Standard commands

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
```

Use the active checkpoint section for any additional commands.

## Test and evidence rules

- Never delete or weaken a test to advance a checkpoint.
- Never claim a command ran unless it ran in the reported environment.
- Never fabricate artifacts or substitute mock output for a real backend.
- Record exact commands, exit codes, hashes, versions, and artifact paths.
- Default CI must not require SeQUeNCe.

## Blockers

Stop and write `docs/blockers/YYYY-MM-DD-short-title.md` when:

- a required command cannot pass within scope;
- authoritative instructions conflict;
- a frozen assumption must change;
- a simulator API, installation, version, or license cannot be verified; or
- unrelated changes would be overwritten.

## Publishing

Do not force-push, tag, publish packages, create a GitHub release, mint a DOI, or make external scientific claims without explicit human authorization.
