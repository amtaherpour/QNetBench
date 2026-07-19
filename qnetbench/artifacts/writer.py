"""Atomic writers for canonical QNetBench result bundles."""

from __future__ import annotations

import csv
import json
import os
import shutil
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import yaml

from qnetbench.artifacts.reader import read_bundle
from qnetbench.errors import ArtifactError, ResultValidationError
from qnetbench.results import (
    ErrorRecord,
    MetricRow,
    RequestResult,
    RunManifest,
    Summary,
    validate_bundle,
)
from qnetbench.spec import BenchmarkSpec, canonical_data

_METRIC_COLUMNS = (
    "metric_id",
    "status",
    "value",
    "unit",
    "population_count",
    "coverage_count",
)


def _json_text(value: Any) -> str:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _write_json(path: Path, model: Any) -> None:
    path.write_text(_json_text(model.model_dump(mode="json")), encoding="utf-8")


def _write_requests(path: Path, requests: Sequence[RequestResult]) -> None:
    lines = [
        json.dumps(
            record.model_dump(mode="json"),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        for record in requests
    ]
    path.write_text(("\n".join(lines) + ("\n" if lines else "")), encoding="utf-8")


def _write_metrics(path: Path, metrics: Sequence[MetricRow]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=_METRIC_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for row in metrics:
            data = row.model_dump(mode="json")
            data["value"] = "" if data["value"] is None else data["value"]
            data["unit"] = "" if data["unit"] is None else data["unit"]
            writer.writerow(data)


def _prepare_destination(destination: Path, overwrite: bool) -> None:
    if destination.exists() and not destination.is_dir():
        raise ArtifactError(f"{destination}: destination must be a directory")
    if destination.exists() and not overwrite:
        raise ArtifactError(
            f"{destination}: destination already exists; use overwrite=True explicitly"
        )
    if destination.parent.exists() and not destination.parent.is_dir():
        raise ArtifactError(f"{destination.parent}: parent is not a directory")
    destination.parent.mkdir(parents=True, exist_ok=True)


def _finalize(temp: Path, destination: Path, overwrite: bool) -> None:
    if not destination.exists():
        os.replace(temp, destination)
        return
    if not overwrite:
        raise ArtifactError(f"{destination}: destination already exists")
    backup = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.backup-",
            dir=destination.parent,
        )
    )
    backup.rmdir()
    os.replace(destination, backup)
    try:
        os.replace(temp, destination)
    except Exception:
        os.replace(backup, destination)
        raise
    shutil.rmtree(backup, ignore_errors=True)


def _write_bundle(
    destination: Path,
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    *,
    requests: Sequence[RequestResult],
    metrics: Sequence[MetricRow],
    summary: Summary | None,
    error: ErrorRecord | None,
    overwrite: bool,
) -> Path:
    _prepare_destination(destination, overwrite)
    try:
        validate_bundle(
            benchmark,
            manifest,
            requests=requests,
            metrics=metrics,
            summary=summary,
            error=error,
        )
    except ResultValidationError as validation_error:
        raise ArtifactError(
            f"refusing to write invalid bundle: {validation_error}"
        ) from validation_error

    temp = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.tmp-",
            dir=destination.parent,
        )
    )
    try:
        benchmark_text = yaml.safe_dump(
            canonical_data(benchmark),
            sort_keys=False,
            allow_unicode=True,
        )
        (temp / "benchmark.yaml").write_text(benchmark_text, encoding="utf-8")
        _write_json(temp / "run_manifest.json", manifest)
        if requests or manifest.status == "complete":
            _write_requests(temp / "requests.jsonl", requests)
        if manifest.status == "complete":
            assert summary is not None
            _write_metrics(temp / "metrics.csv", metrics)
            _write_json(temp / "summary.json", summary)
        else:
            assert error is not None
            _write_json(temp / "error.json", error)
        read_bundle(temp)
        _finalize(temp, destination, overwrite)
        return destination
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def write_complete_bundle(
    destination: str | Path,
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    requests: Sequence[RequestResult],
    metrics: Sequence[MetricRow],
    summary: Summary,
    *,
    overwrite: bool = False,
) -> Path:
    """Atomically write and revalidate a complete canonical bundle."""
    return _write_bundle(
        Path(destination),
        benchmark,
        manifest,
        requests=requests,
        metrics=metrics,
        summary=summary,
        error=None,
        overwrite=overwrite,
    )


def write_failed_bundle(
    destination: str | Path,
    benchmark: BenchmarkSpec,
    manifest: RunManifest,
    error: ErrorRecord,
    *,
    requests: Sequence[RequestResult] = (),
    overwrite: bool = False,
) -> Path:
    """Atomically write and revalidate a failed canonical bundle."""
    return _write_bundle(
        Path(destination),
        benchmark,
        manifest,
        requests=requests,
        metrics=(),
        summary=None,
        error=error,
        overwrite=overwrite,
    )
