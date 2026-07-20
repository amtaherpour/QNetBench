"""Deterministic aggregation of standard metric rows across finite sweeps."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean, stdev
from typing import Any

from qnetbench.artifacts import read_bundle
from qnetbench.errors import SweepError
from qnetbench.results import MetricRow

AGGREGATE_COLUMNS = (
    "parameters_json",
    "metric_id",
    "unit",
    "n_runs",
    "n_ok",
    "mean",
    "sample_std",
    "minimum",
    "maximum",
)


@dataclass(frozen=True)
class RunMetricSet:
    """Metric rows associated with one explicit parameter combination."""

    parameters: dict[str, Any]
    metrics: tuple[MetricRow, ...]


@dataclass(frozen=True)
class AggregateRow:
    """One parameter-group/metric aggregate row."""

    parameters_json: str
    metric_id: str
    unit: str | None
    n_runs: int
    n_ok: int
    mean: float | None
    sample_std: float | None
    minimum: float | None
    maximum: float | None

    @property
    def parameters(self) -> dict[str, Any]:
        value = json.loads(self.parameters_json)
        if not isinstance(value, dict):  # pragma: no cover - defensive
            raise SweepError("aggregate parameters_json must decode to a mapping")
        return value


def _canonical_parameters(parameters: dict[str, Any]) -> str:
    return json.dumps(
        parameters,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def aggregate_metric_sets(
    run_sets: tuple[RunMetricSet, ...],
) -> tuple[AggregateRow, ...]:
    """Aggregate in first-seen group order and canonical per-run metric order."""
    if not run_sets:
        raise SweepError("cannot aggregate an empty sweep")
    groups: dict[str, list[RunMetricSet]] = {}
    for run_set in run_sets:
        key = _canonical_parameters(run_set.parameters)
        groups.setdefault(key, []).append(run_set)

    rows: list[AggregateRow] = []
    for parameters_json, group in groups.items():
        metric_ids = tuple(row.metric_id for row in group[0].metrics)
        if len(metric_ids) != len(set(metric_ids)):
            raise SweepError("a run contains duplicate metric IDs")
        for run_set in group[1:]:
            if tuple(row.metric_id for row in run_set.metrics) != metric_ids:
                raise SweepError(
                    "all sweep runs must expose identical metric IDs/order"
                )
        for metric_index, metric_id in enumerate(metric_ids):
            metric_rows = [run_set.metrics[metric_index] for run_set in group]
            units = {row.unit for row in metric_rows}
            if len(units) != 1:
                raise SweepError(f"metric {metric_id!r} has inconsistent units")
            values = [
                float(row.value)
                for row in metric_rows
                if row.status == "ok" and row.value is not None
            ]
            if any(not math.isfinite(value) for value in values):
                raise SweepError(f"metric {metric_id!r} contains a non-finite value")
            rows.append(
                AggregateRow(
                    parameters_json=parameters_json,
                    metric_id=metric_id,
                    unit=metric_rows[0].unit,
                    n_runs=len(metric_rows),
                    n_ok=len(values),
                    mean=fmean(values) if values else None,
                    sample_std=stdev(values) if len(values) >= 2 else None,
                    minimum=min(values) if values else None,
                    maximum=max(values) if values else None,
                )
            )
    return tuple(rows)


def _format_float(value: float | None) -> str:
    return "" if value is None else format(value, ".17g")


def write_aggregate_csv(path: str | Path, rows: tuple[AggregateRow, ...]) -> Path:
    """Write the stable alpha aggregate table."""
    destination = Path(path)
    try:
        with destination.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=AGGREGATE_COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "parameters_json": row.parameters_json,
                        "metric_id": row.metric_id,
                        "unit": "" if row.unit is None else row.unit,
                        "n_runs": row.n_runs,
                        "n_ok": row.n_ok,
                        "mean": _format_float(row.mean),
                        "sample_std": _format_float(row.sample_std),
                        "minimum": _format_float(row.minimum),
                        "maximum": _format_float(row.maximum),
                    }
                )
    except (OSError, UnicodeError, csv.Error) as error:
        raise SweepError(
            f"{destination}: could not write aggregate CSV: {error}"
        ) from error
    return destination


def read_aggregate_csv(path: str | Path) -> tuple[AggregateRow, ...]:
    """Read and validate the deterministic aggregate table."""
    source = Path(path)
    rows: list[AggregateRow] = []
    try:
        with source.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != AGGREGATE_COLUMNS:
                raise SweepError(
                    f"{source}: expected columns {','.join(AGGREGATE_COLUMNS)}"
                )
            for line_number, raw in enumerate(reader, start=2):
                try:
                    parameters = json.loads(raw["parameters_json"])
                    if not isinstance(parameters, dict):
                        raise ValueError("parameters_json is not a mapping")
                    values: dict[str, float | None] = {}
                    for name in ("mean", "sample_std", "minimum", "maximum"):
                        value = None if raw[name] == "" else float(raw[name])
                        if value is not None and not math.isfinite(value):
                            raise ValueError(f"{name} is non-finite")
                        values[name] = value
                    rows.append(
                        AggregateRow(
                            parameters_json=_canonical_parameters(parameters),
                            metric_id=raw["metric_id"],
                            unit=None if raw["unit"] == "" else raw["unit"],
                            n_runs=int(raw["n_runs"]),
                            n_ok=int(raw["n_ok"]),
                            mean=values["mean"],
                            sample_std=values["sample_std"],
                            minimum=values["minimum"],
                            maximum=values["maximum"],
                        )
                    )
                except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                    raise SweepError(
                        f"{source}:{line_number}: invalid aggregate row: {error}"
                    ) from error
    except SweepError:
        raise
    except (OSError, UnicodeError, csv.Error) as error:
        raise SweepError(f"{source}: could not read aggregate CSV: {error}") from error
    return tuple(rows)


def load_sweep_metric_sets(root: str | Path) -> tuple[RunMetricSet, ...]:
    """Load run parameters and validated metric rows from a sweep directory."""
    directory = Path(root)
    manifest_path = directory / "sweep_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SweepError(
            f"{manifest_path}: could not read sweep manifest: {error}"
        ) from error
    if not isinstance(manifest, dict) or manifest.get("status") != "complete":
        raise SweepError(f"{manifest_path}: sweep manifest is not complete")
    runs = manifest.get("runs")
    if not isinstance(runs, list):
        raise SweepError(f"{manifest_path}: runs must be a list")
    if manifest.get("completed_run_count") != len(runs):
        raise SweepError(f"{manifest_path}: completed run count mismatch")
    run_sets: list[RunMetricSet] = []
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise SweepError(f"{manifest_path}: runs[{index}] must be a mapping")
        parameters = run.get("parameters")
        relative_path = run.get("relative_path")
        if not isinstance(parameters, dict) or not isinstance(relative_path, str):
            raise SweepError(f"{manifest_path}: invalid runs[{index}] entry")
        bundle = read_bundle(directory / relative_path)
        if bundle.manifest.status != "complete":
            raise SweepError(f"{relative_path}: aggregate input run is not complete")
        if bundle.manifest.execution_hash != run.get("execution_hash"):
            raise SweepError(f"{relative_path}: execution hash mismatch")
        run_sets.append(RunMetricSet(parameters=parameters, metrics=bundle.metrics))
    return tuple(run_sets)


def aggregate_sweep(root: str | Path) -> tuple[AggregateRow, ...]:
    """Recompute and write aggregate_metrics.csv from canonical child bundles."""
    directory = Path(root)
    rows = aggregate_metric_sets(load_sweep_metric_sets(directory))
    write_aggregate_csv(directory / "aggregate_metrics.csv", rows)
    return rows
