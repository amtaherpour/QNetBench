# QNetBench

QNetBench is a Python benchmark and reproducibility layer above quantum-network simulators. It is **not** a simulator.

## Current status

The repository is implementing **Checkpoint 2: benchmark loading, normalization, and hashing**.

Available now:

- frozen BenchmarkSpec, canonical-result, and metric contracts at version 0.1;
- strict Pydantic v2 runtime models for BenchmarkSpec v0.1;
- safe YAML/JSON benchmark loading with typed configuration errors;
- deterministic canonical JSON and SHA-256 benchmark hashing;
- Python 3.12 CI with contract, specification, and full-suite checks.

Not implemented yet: result artifact I/O, adapters, metric computation, runners, CLI commands, the benchmark catalog, sweeps, plots, or SeQUeNCe integration.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/contracts
python -m pytest -q tests/spec
python -m pytest -q
git diff --check
```

## Planning documents

Authoritative project guidance is stored under `docs/planning/`. Read `AGENTS.md` and `PROJECT_STATE.md` before making changes.

## License

BSD-3-Clause. See `LICENSE`.
