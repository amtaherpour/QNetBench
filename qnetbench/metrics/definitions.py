"""Frozen standard metric registry for contract version 0.1."""

from qnetbench.metrics.models import MetricDefinition

STANDARD_METRICS: tuple[MetricDefinition, ...] = (
    MetricDefinition("request_success_probability", "1", "planned requests"),
    MetricDefinition("latency_mean_s", "s", "successful requests"),
    MetricDefinition("latency_median_s", "s", "successful requests"),
    MetricDefinition("latency_p95_s", "s", "successful requests"),
    MetricDefinition("fidelity_mean", "1", "successful requests"),
    MetricDefinition("fidelity_median", "1", "successful requests"),
    MetricDefinition(
        "throughput_success_per_s", "success/s", "manifest measurement window"
    ),
    MetricDefinition("attempts_per_success", "attempt/success", "planned requests"),
)
METRIC_DEFINITIONS = {
    definition.metric_id: definition for definition in STANDARD_METRICS
}
METRIC_IDS = tuple(definition.metric_id for definition in STANDARD_METRICS)
