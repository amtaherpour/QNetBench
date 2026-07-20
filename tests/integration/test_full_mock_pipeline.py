from __future__ import annotations

from pathlib import Path

from qnetbench.analysis import plot_sweep, read_aggregate_csv
from qnetbench.artifacts import read_bundle
from qnetbench.catalog import catalog_entries
from qnetbench.metrics import compute_metrics
from qnetbench.runners import RunRequest, SweepRequest, run_single, run_sweep


def test_full_mock_pipeline_gate(tmp_path: Path) -> None:
    for entry in catalog_entries():
        output = tmp_path / "single" / entry.filename.removesuffix(".yaml")
        run_single(RunRequest(entry.path, "mock", 11, output))
        bundle = read_bundle(output)
        recomputed = compute_metrics(
            bundle.manifest,
            bundle.requests,
            bundle.benchmark.requested_metrics,
        )
        assert recomputed == bundle.metrics

    sweep_output = tmp_path / "sweep"
    run_sweep(
        SweepRequest(
            Path("sweeps/v0_1/link_loss_small.yaml"),
            "mock",
            sweep_output,
        )
    )
    rows = read_aggregate_csv(sweep_output / "aggregate_metrics.csv")
    assert len(rows) == 24
    plots = plot_sweep(sweep_output)
    assert len(plots) == 2
