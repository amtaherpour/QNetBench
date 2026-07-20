"""Minimal approved plots derived only from aggregate_metrics.csv."""

from __future__ import annotations

from pathlib import Path

from qnetbench.analysis.aggregate import AggregateRow, read_aggregate_csv
from qnetbench.errors import SweepError

APPROVED_PLOTS = (
    ("request_success_probability", "request_success_probability.png"),
    ("latency_mean_s", "latency_mean_s.png"),
)


def _axis(rows: tuple[AggregateRow, ...]) -> tuple[str, list[float]]:
    parameter_maps = [row.parameters for row in rows]
    keys = {tuple(parameters) for parameters in parameter_maps}
    if not keys or any(len(key) != 1 for key in keys):
        raise SweepError("approved alpha plots require exactly one parameter axis")
    axis_names = {key[0] for key in keys}
    if len(axis_names) != 1:
        raise SweepError("aggregate rows use inconsistent parameter axes")
    axis_name = next(iter(axis_names))
    values: list[float] = []
    for parameters in parameter_maps:
        value = parameters[axis_name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise SweepError("approved alpha plot axis must be numeric")
        values.append(float(value))
    return axis_name, values


def plot_sweep(root: str | Path) -> tuple[Path, ...]:
    """Create only the two approved alpha plots from the aggregate CSV."""
    directory = Path(root)
    rows = read_aggregate_csv(directory / "aggregate_metrics.csv")
    plots_directory = directory / "plots"
    if plots_directory.exists():
        raise SweepError(f"{plots_directory}: plots directory already exists")
    plots_directory.mkdir(parents=False)

    try:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
    except ImportError as error:  # pragma: no cover - dependency environment
        plots_directory.rmdir()
        raise SweepError(
            "plotting requires the optional 'plot' dependency extra"
        ) from error

    created: list[Path] = []
    try:
        for metric_id, filename in APPROVED_PLOTS:
            metric_rows = tuple(row for row in rows if row.metric_id == metric_id)
            if not metric_rows:
                raise SweepError(f"aggregate table has no {metric_id!r} rows")
            axis_name, x_values = _axis(metric_rows)
            points = sorted(
                (
                    x,
                    row.mean,
                )
                for x, row in zip(x_values, metric_rows)
                if row.mean is not None
            )
            if not points:
                raise SweepError(f"metric {metric_id!r} has no available means")
            figure, axes = plt.subplots()
            axes.plot([point[0] for point in points], [point[1] for point in points])
            axes.set_xlabel(axis_name)
            axes.set_ylabel(metric_id)
            axes.set_title(f"{metric_id} vs {axis_name}")
            axes.grid(True)
            destination = plots_directory / filename
            figure.savefig(destination, dpi=150, bbox_inches="tight")
            plt.close(figure)
            created.append(destination)
    except Exception:
        for path in created:
            path.unlink(missing_ok=True)
        try:
            plots_directory.rmdir()
        except OSError:
            pass
        raise
    return tuple(created)
