"""Metric registry models independent of any backend."""

from __future__ import annotations

from dataclasses import dataclass

from qnetbench.results import MetricRow


@dataclass(frozen=True)
class MetricDefinition:
    """Stable metadata for one v0.1 standard metric."""

    metric_id: str
    unit: str
    population: str


__all__ = ["MetricDefinition", "MetricRow"]
