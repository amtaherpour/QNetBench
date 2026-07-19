"""Minimal QNetBench command-line interface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import NoReturn

import typer

from qnetbench.artifacts import read_bundle
from qnetbench.errors import QNetBenchError
from qnetbench.runners import RunRequest, run_single
from qnetbench.spec import benchmark_hash, load_benchmark

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Validate and run reproducible quantum-network benchmarks.",
)


def _fail(error: BaseException) -> NoReturn:
    typer.echo(f"Error: {error}", err=True)
    raise typer.Exit(code=1)


@app.command()
def validate(benchmark: Path) -> None:
    """Validate one benchmark and print its stable hash."""
    try:
        spec = load_benchmark(benchmark)
    except QNetBenchError as error:
        _fail(error)
    typer.echo(f"VALID {spec.benchmark_id} {benchmark_hash(spec)}")


@app.command("run")
def run_command(
    benchmark: Path,
    backend: str = typer.Option(..., "--backend"),
    seed: int = typer.Option(..., "--seed"),
    output: Path = typer.Option(..., "--out"),
    overwrite: bool = typer.Option(False, "--overwrite"),
) -> None:
    """Execute one benchmark through one named adapter."""
    try:
        path = run_single(
            RunRequest(
                benchmark_source=benchmark,
                backend=backend,
                seed=seed,
                output=output,
                overwrite=overwrite,
            )
        )
        bundle = read_bundle(path)
    except QNetBenchError as error:
        _fail(error)
    typer.echo(f"COMPLETE {bundle.manifest.run_id} {path}")


@app.command()
def summarize(bundle: Path) -> None:
    """Print a saved bundle's validated metric rows without re-executing it."""
    try:
        loaded = read_bundle(bundle)
    except QNetBenchError as error:
        _fail(error)
    payload = {
        "run_id": loaded.manifest.run_id,
        "status": loaded.manifest.status,
        "metrics": {row.metric_id: row.value for row in loaded.metrics},
    }
    typer.echo(json.dumps(payload, sort_keys=True, separators=(",", ":")))


@app.command("validate-result")
def validate_result(bundle: Path) -> None:
    """Validate one complete or failed canonical result bundle."""
    try:
        loaded = read_bundle(bundle)
    except QNetBenchError as error:
        _fail(error)
    typer.echo(f"VALID {loaded.manifest.run_id} {loaded.manifest.status}")


if __name__ == "__main__":
    app()
