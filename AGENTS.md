# AGENTS.md - QNetBench

## Mission
QNetBench is a benchmark and reproducibility layer above quantum-network simulators. It is not a simulator.

## Read before editing
1. PROJECT_STATE.md
2. docs/contracts/ and schemas/v0_1/ when they exist
3. QNetBench_Improved_AI_Handoff_Manual_v0_2.md
4. QNetBench_Codex_Execution_Control_Plan_v0_1.md
5. Latest docs/ai_handoff/checkpoint_*_report.md
6. Open docs/blockers/ and relevant docs/decisions/ ADRs when they exist

## Work control
- Work on exactly one active checkpoint.
- Preserve unrelated human changes.
- Run all commands required by the active checkpoint.
- Update PROJECT_STATE.md and write a checkpoint or blocker report.
- Stop after reporting. Do not start the next checkpoint without a new human instruction.

## Architectural invariants
- BenchmarkSpec is backend-independent. Backend, seed, output, and sweeps are execution concerns.
- Canonical result records and the run manifest are the only metric inputs.
- Metrics must never import adapters or read raw backend output.
- Simulator-specific imports and API calls stay in qnetbench/adapters/<name>.py or an approved tools/research/ script.
- Adapters report unsupported fields explicitly; no silent coercion or fallback.
- The mock adapter is synthetic and must complete end to end before SeQUeNCe.
- Do not create qnetbench/adapters/sequence.py before Checkpoint 10.
- Do not change frozen contracts, hashes, benchmark values, or metric semantics without explicit approval and an ADR/version decision.

## Alpha scope
Target release: 0.1.0a1 after Checkpoint 11.
Required backends: mock; SeQUeNCe for link-2 and chain-3 only.
Required catalog: link-2, chain-3, chain-5, grid-3x3.
Out of scope before approval: new simulators, purification, random/adaptive routing, dynamic arrivals, generalized resource metrics, parallel/resumable sweeps, dashboards, paper publication, DOI creation, and additional adapters.

## Standard commands
```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
```

Use the checkpoint section for additional commands.

## Test and evidence rules
- Never delete or weaken a test to advance a checkpoint.
- Never claim a command ran unless it ran in the current environment.
- Never fabricate artifacts or substitute mock output for a real backend.
- Record exact commands, exit codes, hashes, versions, and artifact paths.
- Default CI must not require SeQUeNCe.

## Blockers
Stop and write docs/blockers/YYYY-MM-DD-short-title.md when:
- a required command cannot pass within scope;
- authoritative instructions conflict;
- a frozen assumption must change;
- a simulator API/install/license cannot be verified; or
- unrelated changes would be overwritten.

## Publishing
Do not push, force-push, tag, publish packages, create a GitHub release, mint a DOI, or make external scientific claims without explicit human authorization.
