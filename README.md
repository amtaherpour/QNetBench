# QNetBench

QNetBench is a planned Python benchmark and reproducibility layer above quantum-network simulators. It is **not** a simulator.

## Current status

The repository is at **Checkpoint 0: repository control plane and minimal package skeleton**.

At this checkpoint:

- the package imports as `qnetbench`;
- the package version is `0.0.0.dev0`;
- Python 3.12 is the required baseline;
- default lint and test automation is present;
- no product behavior is implemented.

The benchmark, result, and metric contracts are still drafts and are not implemented. There is no CLI, adapter, simulator dependency, metric engine, runner, benchmark catalog, sweep support, or plotting support yet.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
```

## Planning documents

Authoritative project guidance is stored under `docs/planning/`:

- `QNetBench_Improved_AI_Handoff_Manual_v0_2.md`
- `QNetBench_Codex_Execution_Control_Plan_v0_1.md`

Read `AGENTS.md` and `PROJECT_STATE.md` before making changes.

## License

BSD-3-Clause. See `LICENSE`.
