from __future__ import annotations

from pathlib import Path

import pytest

from qnetbench.analysis import AggregateRow, plot_sweep, write_aggregate_csv
from qnetbench.errors import SweepError


def _row(parameter: float, metric_id: str, value: float) -> AggregateRow:
    return AggregateRow(
        parameters_json=(
            '{"physical_profile.fiber_attenuation_db_per_km":'
            f"{parameter}" + "}"
        ),
        metric_id=metric_id,
        unit="1" if metric_id == "request_success_probability" else "s",
        n_runs=3,
        n_ok=3,
        mean=value,
        sample_std=0.1,
        minimum=value - 0.1,
        maximum=value + 0.1,
    )


def test_plot_creates_only_two_approved_png_files(tmp_path: Path) -> None:
    rows = tuple(
        _row(parameter, metric_id, value)
        for parameter, success, latency in ((0.1, 0.8, 0.01), (0.2, 0.6, 0.02))
        for metric_id, value in (
            ("request_success_probability", success),
            ("latency_mean_s", latency),
        )
    )
    write_aggregate_csv(tmp_path / "aggregate_metrics.csv", rows)
    paths = plot_sweep(tmp_path)
    assert {path.name for path in paths} == {
        "request_success_probability.png",
        "latency_mean_s.png",
    }
    assert all(path.stat().st_size > 0 for path in paths)
    assert {path.name for path in (tmp_path / "plots").iterdir()} == {
        "request_success_probability.png",
        "latency_mean_s.png",
    }
    with pytest.raises(SweepError, match="already exists"):
        plot_sweep(tmp_path)
