"""Deterministic synthetic mock adapter.

The mock is a contract and orchestration oracle. Its values are synthetic and are
not a physical model or a physics baseline.
"""

from __future__ import annotations

import hashlib
import heapq
from dataclasses import dataclass

from qnetbench.adapters.base import Adapter, AdapterRun, BackendIdentity, SupportReport
from qnetbench.results import RequestResult
from qnetbench.spec import BenchmarkSpec

MOCK_ALGORITHM_VERSION = "1.0"
_IDENTITY = BackendIdentity(
    adapter_name="mock",
    adapter_version="0.1",
    backend_name="mock",
    backend_version=MOCK_ALGORITHM_VERSION,
)


@dataclass(frozen=True)
class _PathInfo:
    nodes: tuple[str, ...]
    length_km: float


def _stable_uint64(*parts: object) -> int:
    text = "\x1f".join(str(part) for part in parts)
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def _uniform(*parts: object) -> float:
    return _stable_uint64(*parts) / 2**64


def _shortest_path(benchmark: BenchmarkSpec) -> _PathInfo:
    source = benchmark.workload.source
    destination = benchmark.workload.destination
    adjacency: dict[str, list[tuple[str, float]]] = {
        node.node_id: [] for node in benchmark.network.nodes
    }
    for link in benchmark.network.links:
        left, right = link.endpoints
        adjacency[left].append((right, link.length_km))
        adjacency[right].append((left, link.length_km))
    for neighbors in adjacency.values():
        neighbors.sort(key=lambda item: item[0])

    queue: list[tuple[float, tuple[str, ...], str]] = [(0.0, (source,), source)]
    best: dict[str, tuple[float, tuple[str, ...]]] = {}
    while queue:
        distance, path, node = heapq.heappop(queue)
        candidate = (distance, path)
        if node in best and best[node] <= candidate:
            continue
        best[node] = candidate
        if node == destination:
            return _PathInfo(path, distance)
        for neighbor, length in adjacency[node]:
            if neighbor in path:
                continue
            heapq.heappush(queue, (distance + length, (*path, neighbor), neighbor))
    raise ValueError(f"no path connects {source!r} to {destination!r}")


def _support_issue(path: str, reason: str) -> tuple[str, str]:
    return path, reason


class MockAdapter(Adapter):
    """Synthetic deterministic adapter supporting the complete alpha subset."""

    @property
    def identity(self) -> BackendIdentity:
        return _IDENTITY

    def check_support(self, benchmark: BenchmarkSpec) -> SupportReport:
        issues: list[tuple[str, str]] = []
        if benchmark.schema_version != "0.1":
            issues.append(_support_issue("schema_version", "mock supports only 0.1"))
        if benchmark.extensions:
            issues.append(
                _support_issue("extensions", "mock supports no alpha extensions")
            )
        if benchmark.protocol.routing != "shortest_path":
            issues.append(
                _support_issue("protocol.routing", "only shortest_path is supported")
            )
        if benchmark.protocol.shortest_path_tiebreak != "lexical":
            issues.append(
                _support_issue(
                    "protocol.shortest_path_tiebreak",
                    "only lexical tie-breaking is supported",
                )
            )
        if benchmark.protocol.purification != "none":
            issues.append(
                _support_issue("protocol.purification", "purification is unsupported")
            )
        try:
            path = _shortest_path(benchmark)
        except ValueError as error:
            issues.append(_support_issue("network.links", str(error)))
        else:
            expected_swapping = "none" if len(path.nodes) == 2 else "sequential"
            if benchmark.protocol.swapping != expected_swapping:
                issues.append(
                    _support_issue(
                        "protocol.swapping",
                        (
                            f"path with {len(path.nodes)} nodes requires "
                            f"{expected_swapping!r}"
                        ),
                    )
                )
        return SupportReport(
            supported=not issues,
            reasons=tuple(reason for _, reason in issues),
            unsupported_paths=tuple(path for path, _ in issues),
            warnings=("mock output is synthetic and not a physics baseline",),
            backend_identity=self.identity,
        )

    def _run_supported(
        self,
        benchmark: BenchmarkSpec,
        *,
        benchmark_hash: str,
        seed: int,
    ) -> AdapterRun:
        path = _shortest_path(benchmark)
        profile = benchmark.physical_profile
        workload = benchmark.workload
        link_count = len(path.nodes) - 1
        swap_count = max(0, len(path.nodes) - 2)

        attenuation = 10 ** (-profile.fiber_attenuation_db_per_km * path.length_km / 10)
        generation_probability = (
            profile.memory_efficiency
            * profile.detector_efficiency
            * attenuation
            * (profile.swap_success_probability**swap_count)
        )
        generation_probability = min(0.98, max(0.02, generation_probability))
        fidelity = min(
            1.0,
            max(
                0.0,
                (profile.link_fidelity**link_count)
                * (profile.swap_fidelity_factor**swap_count),
            ),
        )
        round_trip_s = 2 * path.length_km / profile.quantum_propagation_speed_km_per_s
        records: list[RequestResult] = []
        for index in range(workload.request_count):
            request_id = f"request-{index + 1:04d}"
            success_draw = _uniform(
                MOCK_ALGORITHM_VERSION,
                benchmark_hash,
                seed,
                request_id,
                "success",
            )
            attempts = 1 + (
                _stable_uint64(
                    MOCK_ALGORITHM_VERSION,
                    benchmark_hash,
                    seed,
                    request_id,
                    "attempts",
                )
                % max(2, 2 * link_count + 3)
            )
            submitted = workload.batch_start_s
            synthetic_latency = round_trip_s + attempts / profile.memory_frequency_hz
            terminal = submitted + synthetic_latency
            succeeded = (
                success_draw < generation_probability
                and terminal <= workload.deadline_s
            )
            if succeeded:
                status = "success"
                failure_reason = None
                record_fidelity: float | None = fidelity
            else:
                status = "timed_out"
                failure_reason = "synthetic deadline outcome"
                record_fidelity = None
                terminal = workload.deadline_s
            records.append(
                RequestResult(
                    request_id=request_id,
                    source=workload.source,
                    destination=workload.destination,
                    submitted_at_s=submitted,
                    terminal_at_s=terminal,
                    status=status,
                    latency_s=terminal - submitted,
                    fidelity=record_fidelity,
                    attempts=int(attempts),
                    path=path.nodes,
                    failure_reason=failure_reason,
                    metadata={
                        "synthetic": True,
                        "mock_algorithm_version": MOCK_ALGORITHM_VERSION,
                        "path_link_count": link_count,
                        "path_swap_count": swap_count,
                        "synthetic_success_probability": generation_probability,
                    },
                )
            )
        return AdapterRun(
            requests=tuple(records),
            measurement_start_s=workload.batch_start_s,
            measurement_end_s=workload.deadline_s,
            backend_identity=self.identity,
            warnings=("mock output is synthetic and not a physics baseline",),
        )
