"""Executable SeQUeNCe 1.0.0 installation and API surface probe."""

from __future__ import annotations

import argparse
import inspect
import json
from importlib.metadata import version
from pathlib import Path

from sequence.app.request_app import RequestApp
from sequence.kernel.timeline import Timeline
from sequence.topology.node import QuantumRouter
from sequence.topology.router_net_topo import RouterNetTopo


def run_probe() -> dict[str, object]:
    """Instantiate the kernel and verify APIs needed for Checkpoint 9 research."""
    installed = version("sequence")
    if installed != "1.0.0":
        raise RuntimeError(f"expected sequence 1.0.0, found {installed}")

    timeline = Timeline(1_000)
    timeline.seed(20260720)
    if timeline.now() != 0:
        raise RuntimeError("new SeQUeNCe timeline did not start at time zero")
    timeline.init()
    timeline.run()

    start_parameters = tuple(inspect.signature(RequestApp.start).parameters)
    required_parameters = {
        "self",
        "responder",
        "start_t",
        "end_t",
        "memo_size",
        "fidelity",
    }
    if not required_parameters.issubset(start_parameters):
        raise RuntimeError(
            "RequestApp.start lacks required request parameters: "
            f"{sorted(required_parameters - set(start_parameters))}"
        )
    if not hasattr(RouterNetTopo, "get_timeline"):
        raise RuntimeError("RouterNetTopo.get_timeline is unavailable")
    if not hasattr(QuantumRouter, "set_seed"):
        raise RuntimeError("QuantumRouter.set_seed is unavailable")

    return {
        "probe_schema_version": "1.0",
        "simulator_id": "sequence",
        "package_version": installed,
        "timeline_constructed": True,
        "timeline_seed_api": True,
        "timeline_empty_run_completed": True,
        "request_app_start_parameters": list(start_parameters),
        "router_topology_api": True,
        "quantum_router_seed_api": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = run_probe()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
