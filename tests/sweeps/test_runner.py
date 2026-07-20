from __future__ import annotations

import json
from pathlib import Path

import pytest

from qnetbench.analysis import read_aggregate_csv
from qnetbench.artifacts import read_bundle
from qnetbench.errors import SweepError
from qnetbench.runners import SweepRequest, run_sweep

SWEEP = Path("sweeps/v0_1/link_loss_small.yaml")


def test_sequential_sweep_writes_manifest_children_and_aggregate(
    tmp_path: Path,
) -> None:
    output = tmp_path / "sweep"
    run_sweep(SweepRequest(SWEEP, "mock", output))
    manifest = json.loads((output / "sweep_manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert manifest["planned_run_count"] == 9
    assert manifest["completed_run_count"] == 9
    assert manifest["parameter_paths"] == [
        "physical_profile.fiber_attenuation_db_per_km"
    ]
    assert manifest["seeds"] == [1, 2, 3]
    assert len({run["execution_hash"] for run in manifest["runs"]}) == 9
    for run in manifest["runs"]:
        bundle = read_bundle(output / run["relative_path"])
        assert bundle.manifest.status == "complete"
        assert bundle.manifest.execution_hash == run["execution_hash"]
    rows = read_aggregate_csv(output / "aggregate_metrics.csv")
    assert len(rows) == 3 * 8
    assert {(row.n_runs, row.n_ok) for row in rows} <= {(3, 3), (3, 0)}
    assert not (output / ".resolved_inputs").exists()


def test_existing_sweep_directory_fails_without_resume_or_overwrite(
    tmp_path: Path,
) -> None:
    output = tmp_path / "existing"
    output.mkdir()
    marker = output / "marker.txt"
    marker.write_text("keep", encoding="utf-8")
    with pytest.raises(SweepError, match="already exists"):
        run_sweep(SweepRequest(SWEEP, "mock", output))
    assert marker.read_text(encoding="utf-8") == "keep"
    assert not list(tmp_path.glob(".existing.tmp-*"))
