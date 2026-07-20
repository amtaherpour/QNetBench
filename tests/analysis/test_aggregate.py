from __future__ import annotations

from qnetbench.analysis import RunMetricSet, aggregate_metric_sets
from qnetbench.results import MetricRow


def _metric(value: float | None, *, status: str = "ok") -> MetricRow:
    return MetricRow(
        metric_id="request_success_probability",
        status=status,
        value=value,
        unit="1",
        population_count=4,
        coverage_count=4 if status == "ok" else 0,
    )


def test_aggregate_reports_n_runs_n_ok_and_sample_statistics() -> None:
    rows = aggregate_metric_sets(
        (
            RunMetricSet({"loss": 0.1}, (_metric(0.25),)),
            RunMetricSet({"loss": 0.1}, (_metric(0.75),)),
            RunMetricSet({"loss": 0.1}, (_metric(None, status="unavailable"),)),
        )
    )
    row = rows[0]
    assert row.n_runs == 3
    assert row.n_ok == 2
    assert row.mean == 0.5
    assert row.sample_std == 0.3535533905932738
    assert row.minimum == 0.25
    assert row.maximum == 0.75


def test_all_unavailable_values_produce_blank_statistics() -> None:
    row = aggregate_metric_sets(
        (
            RunMetricSet({"loss": 0.2}, (_metric(None, status="unavailable"),)),
            RunMetricSet({"loss": 0.2}, (_metric(None, status="unavailable"),)),
        )
    )[0]
    assert row.n_runs == 2
    assert row.n_ok == 0
    assert row.mean is None
    assert row.sample_std is None
    assert row.minimum is None
    assert row.maximum is None
