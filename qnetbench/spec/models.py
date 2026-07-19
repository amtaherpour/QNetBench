"""Strict runtime models for BenchmarkSpec v0.1."""

from __future__ import annotations

import math
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StringConstraints,
    field_validator,
    model_validator,
)

_IDENTIFIER_PATTERN = r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"

Identifier = Annotated[
    str,
    StringConstraints(pattern=_IDENTIFIER_PATTERN),
]
PositiveFiniteFloat = Annotated[FiniteFloat, Field(gt=0)]
NonNegativeFiniteFloat = Annotated[FiniteFloat, Field(ge=0)]
Probability = Annotated[FiniteFloat, Field(ge=0, le=1)]
PositiveInt = Annotated[int, Field(ge=1)]
MetricId = Literal[
    "request_success_probability",
    "latency_mean_s",
    "latency_median_s",
    "latency_p95_s",
    "fidelity_mean",
    "fidelity_median",
    "throughput_success_per_s",
    "attempts_per_success",
]


class StrictModel(BaseModel):
    """Shared strict configuration for all contract models."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        validate_default=True,
    )


class NodeSpec(StrictModel):
    """One explicitly identified network node."""

    node_id: Identifier


class LinkSpec(StrictModel):
    """One undirected quantum link."""

    link_id: Identifier
    endpoints: tuple[Identifier, Identifier]
    length_km: PositiveFiniteFloat

    @field_validator("endpoints", mode="before")
    @classmethod
    def normalize_endpoints(cls, value: object) -> object:
        """Accept the JSON/YAML array encoding and store it immutably."""
        return tuple(value) if isinstance(value, list) else value

    @model_validator(mode="after")
    def validate_endpoints(self) -> LinkSpec:
        """Require two distinct endpoints."""
        if self.endpoints[0] == self.endpoints[1]:
            raise ValueError("endpoints[1] must differ from endpoints[0]")
        return self


class NetworkSpec(StrictModel):
    """Explicit static network topology."""

    nodes: tuple[NodeSpec, ...] = Field(min_length=2)
    links: tuple[LinkSpec, ...] = Field(min_length=1)

    @field_validator("nodes", "links", mode="before")
    @classmethod
    def normalize_sequences(cls, value: object) -> object:
        """Accept JSON/YAML arrays and store them immutably."""
        return tuple(value) if isinstance(value, list) else value

    @model_validator(mode="after")
    def validate_identifiers_and_references(self) -> NetworkSpec:
        """Require unique IDs and valid endpoint references."""
        node_positions: dict[str, int] = {}
        for index, node in enumerate(self.nodes):
            if node.node_id in node_positions:
                first = node_positions[node.node_id]
                raise ValueError(
                    f"nodes[{index}].node_id duplicates nodes[{first}].node_id"
                )
            node_positions[node.node_id] = index

        link_positions: dict[str, int] = {}
        for index, link in enumerate(self.links):
            if link.link_id in link_positions:
                first = link_positions[link.link_id]
                raise ValueError(
                    f"links[{index}].link_id duplicates links[{first}].link_id"
                )
            link_positions[link.link_id] = index
            for endpoint_index, endpoint in enumerate(link.endpoints):
                if endpoint not in node_positions:
                    raise ValueError(
                        f"links[{index}].endpoints[{endpoint_index}] references "
                        f"unknown node_id {endpoint!r}"
                    )
        return self


class PhysicalProfile(StrictModel):
    """Common physical parameters frozen for the alpha contract."""

    memory_count_per_node: PositiveInt
    memory_coherence_time_s: PositiveFiniteFloat
    memory_frequency_hz: PositiveFiniteFloat
    memory_efficiency: Probability
    detector_efficiency: Probability
    fiber_attenuation_db_per_km: NonNegativeFiniteFloat
    quantum_propagation_speed_km_per_s: PositiveFiniteFloat
    classical_propagation_speed_km_per_s: PositiveFiniteFloat
    link_fidelity: Probability
    swap_success_probability: Probability
    swap_fidelity_factor: Probability


class WorkloadSpec(StrictModel):
    """Finite batch entanglement-distribution workload."""

    source: Identifier
    destination: Identifier
    request_count: PositiveInt
    batch_start_s: NonNegativeFiniteFloat
    deadline_s: PositiveFiniteFloat

    @model_validator(mode="after")
    def validate_timing_and_endpoints(self) -> WorkloadSpec:
        """Require a meaningful interval and distinct endpoints."""
        if self.source == self.destination:
            raise ValueError("destination must differ from source")
        if self.deadline_s <= self.batch_start_s:
            raise ValueError("deadline_s must be greater than batch_start_s")
        return self


class ProtocolSpec(StrictModel):
    """Deterministic alpha protocol choices."""

    routing: Literal["shortest_path"]
    shortest_path_tiebreak: Literal["lexical"]
    swapping: Literal["none", "sequential"]
    purification: Literal["none"]


class BenchmarkSpec(StrictModel):
    """Backend-independent BenchmarkSpec v0.1."""

    schema_version: Literal["0.1"]
    benchmark_id: Identifier
    title: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[str, StringConstraints(min_length=1)]
    network: NetworkSpec
    physical_profile: PhysicalProfile
    workload: WorkloadSpec
    protocol: ProtocolSpec
    requested_metrics: tuple[MetricId, ...] = Field(min_length=1)
    extensions: dict[str, Any]

    @field_validator("requested_metrics", mode="before")
    @classmethod
    def normalize_requested_metrics(cls, value: object) -> object:
        """Accept the contract array encoding and store it immutably."""
        return tuple(value) if isinstance(value, list) else value

    @model_validator(mode="after")
    def validate_cross_field_contract(self) -> BenchmarkSpec:
        """Apply invariants that span BenchmarkSpec sections."""
        if self.extensions:
            key = next(iter(self.extensions))
            raise ValueError(f"extensions.{key} is not allowed in v0.1 alpha")

        if len(self.requested_metrics) != len(set(self.requested_metrics)):
            raise ValueError("requested_metrics contains a duplicate metric ID")

        node_ids = {node.node_id for node in self.network.nodes}
        if self.workload.source not in node_ids:
            raise ValueError(
                f"workload.source references unknown node_id {self.workload.source!r}"
            )
        if self.workload.destination not in node_ids:
            raise ValueError(
                "workload.destination references unknown node_id "
                f"{self.workload.destination!r}"
            )
        return self

    @model_validator(mode="after")
    def validate_finite_values(self) -> BenchmarkSpec:
        """Defensively reject any non-finite number in the normalized model."""

        def visit(value: object) -> None:
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("non-finite numeric value is not allowed")
            if isinstance(value, dict):
                for item in value.values():
                    visit(item)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    visit(item)

        visit(self.model_dump(mode="python"))
        return self
