"""Executable semantic-mapping probe for SeQUeNCe 1.0.0.

This is Checkpoint 9 research evidence, not a production adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import networkx as nx
from sequence.app.request_app import RequestApp
from sequence.constants import DENSITY_MATRIX_FORMALISM, SINGLE_HERALDED
from sequence.entanglement_management.generation import (
    EntanglementGenerationA,
    EntanglementGenerationB,
)
from sequence.topology.router_net_topo import RouterNetTopo
from sequence.utils.nx_converter import generate_config

from qnetbench.results import RequestResult
from qnetbench.spec import BenchmarkSpec, benchmark_hash, load_benchmark

PS_PER_SECOND = 10**12
CONTROL_LEAD_S = 0.01
TARGET_FIDELITY = 0.5


class RecordingRequestApp(RequestApp):
    """Record native successful entanglement events exposed by RequestApp."""

    def __init__(self, node: Any, *, limit: int, inverse_names: dict[str, str]):
        super().__init__(node)
        self.limit = limit
        self.inverse_names = inverse_names
        self.events: list[dict[str, Any]] = []
        self.reservation_events: list[dict[str, Any]] = []

    def get_reservation_result(self, reservation: Any, result: bool) -> None:
        self.reservation_events.append(
            {
                "native_time_ps": int(self.node.timeline.now()),
                "approved": bool(result),
                "path": [
                    self.inverse_names.get(name, name) for name in reservation.path
                ],
            }
        )
        super().get_reservation_result(reservation, result)

    def get_memory(self, info: Any) -> None:
        if (
            len(self.events) < self.limit
            and info.state == "ENTANGLED"
            and info.index in self.memo_to_reservation
        ):
            reservation = self.memo_to_reservation[info.index]
            if (
                info.remote_node == reservation.responder
                and info.fidelity >= reservation.fidelity
            ):
                self.events.append(
                    {
                        "native_time_ps": int(info.entangle_time),
                        "callback_time_ps": int(self.node.timeline.now()),
                        "memory_index": int(info.index),
                        "fidelity": float(info.fidelity),
                        "path": [
                            self.inverse_names.get(name, name)
                            for name in reservation.path
                        ],
                    }
                )
        super().get_memory(info)


def _build_graph(spec: BenchmarkSpec) -> nx.Graph:
    graph = nx.Graph()
    for node in spec.network.nodes:
        graph.add_node(node.node_id)
    attenuation = spec.physical_profile.fiber_attenuation_db_per_km / 1000.0
    for link in spec.network.links:
        graph.add_edge(
            link.endpoints[0],
            link.endpoints[1],
            length=link.length_km,
            attenuation=attenuation,
        )
    return graph


def _node_template(
    spec: BenchmarkSpec,
    detector_efficiency: float,
) -> dict[str, Any]:
    profile = spec.physical_profile
    detector = {
        "efficiency": detector_efficiency,
        "dark_count": 0,
        "time_resolution": 1,
        "count_rate": 100_000_000_000.0,
    }
    return {
        "router_template": {
            "MemoryArray": {
                "frequency": profile.memory_frequency_hz,
                "coherence_time": profile.memory_coherence_time_s,
                "efficiency": profile.memory_efficiency,
                "fidelity": profile.link_fidelity,
            }
        },
        "bsm_template": {
            "encoding_type": "single_heralded",
            "SingleHeraldedBSM": {
                "detectors": [detector.copy(), detector.copy()]
            },
        },
    }


def _shortest_path(spec: BenchmarkSpec) -> tuple[str, ...]:
    graph = nx.Graph()
    for link in spec.network.links:
        graph.add_edge(
            link.endpoints[0],
            link.endpoints[1],
            weight=link.length_km,
        )
    candidates = nx.all_shortest_paths(
        graph,
        spec.workload.source,
        spec.workload.destination,
        weight="weight",
    )
    return min(tuple(path) for path in candidates)


def _patch_config(
    config: dict[str, Any],
    *,
    graph: nx.Graph,
    graph_to_name: dict[str, str],
    seed: int,
    classical_speed_km_s: float,
) -> None:
    for index, node in enumerate(config["nodes"]):
        node["seed"] = seed * 10_000 + index

    inverse_names = {name: node_id for node_id, name in graph_to_name.items()}
    speed_m_ps = classical_speed_km_s * 1e-9
    for channel in config["cchannels"]:
        if "distance" in channel:
            channel["delay"] = int(round(channel["distance"] / speed_m_ps))
            continue
        source = inverse_names[channel["source"]]
        destination = inverse_names[channel["destination"]]
        distance_km = nx.shortest_path_length(
            graph,
            source,
            destination,
            weight="length",
        )
        channel["delay"] = int(
            round(distance_km / classical_speed_km_s * PS_PER_SECOND)
        )


def _records_from_events(
    spec: BenchmarkSpec,
    events: list[dict[str, Any]],
) -> tuple[RequestResult, ...]:
    expected_path = _shortest_path(spec)
    control_offset_ps = int(round(CONTROL_LEAD_S * PS_PER_SECOND))
    records: list[RequestResult] = []
    for index in range(spec.workload.request_count):
        request_id = f"request-{index + 1:04d}"
        if index < len(events):
            event = events[index]
            terminal = (
                event["native_time_ps"] - control_offset_ps
            ) / PS_PER_SECOND
            terminal = max(spec.workload.batch_start_s, terminal)
            terminal = min(spec.workload.deadline_s, terminal)
            records.append(
                RequestResult(
                    request_id=request_id,
                    source=spec.workload.source,
                    destination=spec.workload.destination,
                    submitted_at_s=spec.workload.batch_start_s,
                    terminal_at_s=terminal,
                    status="success",
                    latency_s=terminal - spec.workload.batch_start_s,
                    fidelity=event["fidelity"],
                    attempts=None,
                    path=tuple(event["path"] or expected_path),
                    failure_reason=None,
                    metadata={
                        "simulator": "sequence",
                        "classification": (
                            "native_event_derived_request_assignment"
                        ),
                        "native_time_ps": event["native_time_ps"],
                        "callback_time_ps": event["callback_time_ps"],
                        "memory_index": event["memory_index"],
                    },
                )
            )
        else:
            records.append(
                RequestResult(
                    request_id=request_id,
                    source=spec.workload.source,
                    destination=spec.workload.destination,
                    submitted_at_s=spec.workload.batch_start_s,
                    terminal_at_s=spec.workload.deadline_s,
                    status="timed_out",
                    latency_s=(
                        spec.workload.deadline_s - spec.workload.batch_start_s
                    ),
                    fidelity=None,
                    attempts=None,
                    path=expected_path,
                    failure_reason="SeQUeNCe reservation window expired",
                    metadata={
                        "simulator": "sequence",
                        "classification": "derived_timeout",
                    },
                )
            )
    return tuple(records)


def run_case(
    benchmark_path: Path,
    *,
    seed: int,
    controlled_failure: bool,
) -> dict[str, Any]:
    spec = load_benchmark(benchmark_path)
    graph = _build_graph(spec)
    detector_efficiency = (
        0.0 if controlled_failure else spec.physical_profile.detector_efficiency
    )
    native_start_ps = int(
        round((CONTROL_LEAD_S + spec.workload.batch_start_s) * PS_PER_SECOND)
    )
    native_end_ps = int(
        round((CONTROL_LEAD_S + spec.workload.deadline_s) * PS_PER_SECOND)
    )

    with tempfile.TemporaryDirectory(prefix="qnetbench-sequence-") as directory:
        config, graph_to_name = generate_config(
            graph,
            cc_delay=0.0,
            memory_size=spec.physical_profile.memory_count_per_node,
            output_file="topology.json",
            output_directory=directory,
            stop_time=CONTROL_LEAD_S + spec.workload.deadline_s + 0.01,
            formalism=DENSITY_MATRIX_FORMALISM,
            node_template=_node_template(spec, detector_efficiency),
        )
        _patch_config(
            config,
            graph=graph,
            graph_to_name=graph_to_name,
            seed=seed,
            classical_speed_km_s=(
                spec.physical_profile.classical_propagation_speed_km_per_s
            ),
        )
        EntanglementGenerationA.set_global_type(SINGLE_HERALDED)
        EntanglementGenerationB.set_global_type(SINGLE_HERALDED)
        topology = RouterNetTopo(config)
        timeline = topology.get_timeline()
        timeline.seed(seed)
        timeline.show_progress = False

        routers = {
            router.name: router
            for router in topology.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER)
        }
        inverse_names = {name: node_id for node_id, name in graph_to_name.items()}
        profile = spec.physical_profile
        for router in routers.values():
            memory_array = router.get_components_by_type("MemoryArray")[0]
            memory_array.update_memory_params("frequency", profile.memory_frequency_hz)
            memory_array.update_memory_params(
                "coherence_time",
                profile.memory_coherence_time_s,
            )
            memory_array.update_memory_params("efficiency", profile.memory_efficiency)
            memory_array.update_memory_params("raw_fidelity", profile.link_fidelity)
            router.swapping_success_prob = profile.swap_success_probability
            router.swapping_degradation = profile.swap_fidelity_factor

        quantum_speed_m_ps = profile.quantum_propagation_speed_km_per_s * 1e-9
        for channel in topology.get_qchannels():
            channel.light_speed = quantum_speed_m_ps
            channel.frequency = profile.memory_frequency_hz

        source_name = graph_to_name[spec.workload.source]
        destination_name = graph_to_name[spec.workload.destination]
        source_app = RecordingRequestApp(
            routers[source_name],
            limit=spec.workload.request_count,
            inverse_names=inverse_names,
        )
        RequestApp(routers[destination_name])
        timeline.init()
        source_app.start(
            responder=destination_name,
            start_t=native_start_ps,
            end_t=native_end_ps,
            memo_size=min(
                profile.memory_count_per_node,
                spec.workload.request_count,
            ),
            fidelity=TARGET_FIDELITY,
        )
        timeline.run()

    records = _records_from_events(spec, source_app.events)
    payload: dict[str, Any] = {
        "probe_schema_version": "1.0",
        "simulator_id": "sequence",
        "simulator_version": "1.0.0",
        "benchmark_path": benchmark_path.as_posix(),
        "benchmark_id": spec.benchmark_id,
        "benchmark_hash": benchmark_hash(spec),
        "seed": seed,
        "controlled_failure": controlled_failure,
        "native_time_unit": "picosecond",
        "canonical_time_offset_s": CONTROL_LEAD_S,
        "simulator_control_target_fidelity": TARGET_FIDELITY,
        "reservation_events": source_app.reservation_events,
        "native_success_event_count": len(source_app.events),
        "records": [record.model_dump(mode="json") for record in records],
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    payload["canonical_digest"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    evidence: dict[str, Any] = {
        "evidence_schema_version": "1.0",
        "simulator_id": "sequence",
        "simulator_version": "1.0.0",
        "cases": {},
    }
    for benchmark_path in (
        Path("benchmarks/v0_1/link_2_batch.yaml"),
        Path("benchmarks/v0_1/chain_3_batch.yaml"),
    ):
        first = run_case(benchmark_path, seed=7, controlled_failure=False)
        repeat = run_case(benchmark_path, seed=7, controlled_failure=False)
        alternate = run_case(benchmark_path, seed=8, controlled_failure=False)
        failure = run_case(benchmark_path, seed=7, controlled_failure=True)
        if first != repeat:
            raise RuntimeError(f"{benchmark_path}: same-seed evidence differs")
        normal_successes = sum(
            record["status"] == "success" for record in first["records"]
        )
        failure_successes = sum(
            record["status"] == "success" for record in failure["records"]
        )
        if normal_successes < 1:
            raise RuntimeError(f"{benchmark_path}: normal probe produced no success")
        if failure_successes != 0:
            raise RuntimeError(
                f"{benchmark_path}: controlled failure produced a success"
            )
        evidence["cases"][first["benchmark_id"]] = {
            "same_seed_identical": True,
            "alternate_seed_digest": alternate["canonical_digest"],
            "normal": first,
            "controlled_failure": failure,
        }

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(evidence, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "passed", "output": str(arguments.output)}))


if __name__ == "__main__":
    main()
