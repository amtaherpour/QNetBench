"""Sequential finite sweep orchestration over the single-run pipeline."""

from __future__ import annotations

import json
import shutil
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from qnetbench.adapters import BackendIdentity, get_adapter
from qnetbench.analysis.aggregate import aggregate_sweep
from qnetbench.artifacts import read_bundle
from qnetbench.errors import QNetBenchError, SweepError
from qnetbench.runners.single import (
    RunRequest,
    execution_hash,
    make_run_id,
    run_single,
)
from qnetbench.sweeps import (
    ExpandedCase,
    LoadedSweep,
    expand_sweep,
    load_sweep,
    sweep_hash,
)


@dataclass(frozen=True)
class SweepRequest:
    """One explicit finite sweep execution request."""

    sweep_source: Path
    backend: str
    output: Path | None = None


@dataclass(frozen=True)
class SweepPlanEntry:
    """One fully resolved child execution in deterministic plan order."""

    case: ExpandedCase
    execution_hash: str
    run_id: str
    relative_path: Path

    @property
    def parameters(self) -> dict[str, Any]:
        return self.case.parameter_map


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def build_sweep_plan(
    loaded: LoadedSweep,
    *,
    backend: str,
) -> tuple[SweepPlanEntry, ...]:
    """Resolve deterministic cases and backend execution hashes before execution."""
    identity: BackendIdentity = get_adapter(backend).identity
    entries: list[SweepPlanEntry] = []
    execution_hashes: set[str] = set()
    for case in expand_sweep(loaded):
        digest = execution_hash(case.benchmark_hash, identity, case.seed)
        if digest in execution_hashes:
            raise SweepError("sweep plan contains a duplicate execution hash")
        execution_hashes.add(digest)
        run_id = make_run_id(
            case.benchmark.benchmark_id,
            identity.backend_name,
            case.seed,
            digest,
        )
        relative_path = Path("runs") / f"{case.index:03d}-{digest[:12]}"
        entries.append(
            SweepPlanEntry(
                case=case,
                execution_hash=digest,
                run_id=run_id,
                relative_path=relative_path,
            )
        )
    return tuple(entries)


def _identity_data(identity: BackendIdentity) -> dict[str, str | None]:
    return {
        "adapter_name": identity.adapter_name,
        "adapter_version": identity.adapter_version,
        "backend_name": identity.backend_name,
        "backend_version": identity.backend_version,
    }


def _manifest_data(
    *,
    loaded: LoadedSweep,
    backend: str,
    identity: BackendIdentity,
    plan: tuple[SweepPlanEntry, ...],
    started_at: str,
    ended_at: str,
) -> dict[str, Any]:
    runs = [
        {
            "index": entry.case.index,
            "parameters": entry.parameters,
            "seed": entry.case.seed,
            "benchmark_hash": entry.case.benchmark_hash,
            "execution_hash": entry.execution_hash,
            "run_id": entry.run_id,
            "relative_path": entry.relative_path.as_posix(),
            "status": "complete",
        }
        for entry in plan
    ]
    return {
        "sweep_schema_version": "0.1",
        "sweep_id": loaded.spec.sweep_id,
        "sweep_hash": sweep_hash(loaded.spec),
        "status": "complete",
        "backend": backend,
        "backend_identity": _identity_data(identity),
        "source": str(loaded.source),
        "base_benchmark": str(loaded.base_benchmark_path),
        "output_root_declared": loaded.spec.output_root,
        "parameter_paths": sorted(axis.path for axis in loaded.spec.axes),
        "seeds": list(loaded.spec.seeds),
        "planned_run_count": len(plan),
        "completed_run_count": len(plan),
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "runs": runs,
    }


def _write_resolved_benchmark(path: Path, entry: SweepPlanEntry) -> None:
    path.write_text(
        yaml.safe_dump(entry.case.benchmark.model_dump(mode="json"), sort_keys=False),
        encoding="utf-8",
    )


def run_sweep(request: SweepRequest) -> Path:
    """Run a bounded plan sequentially and finalize one validated sweep directory."""
    loaded = load_sweep(request.sweep_source)
    output = loaded.default_output_path if request.output is None else request.output
    output = Path(output)
    if output.exists():
        raise SweepError(f"{output}: sweep destination already exists")
    output.parent.mkdir(parents=True, exist_ok=True)

    identity = get_adapter(request.backend).identity
    plan = build_sweep_plan(loaded, backend=request.backend)
    temp = output.parent / f".{output.name}.tmp-{uuid.uuid4().hex}"
    if temp.exists():  # pragma: no cover - UUID collision defense
        raise SweepError(f"temporary sweep path unexpectedly exists: {temp}")
    started_at = _utc_now()
    inputs = temp / ".resolved_inputs"
    try:
        inputs.mkdir(parents=True)
        (temp / "runs").mkdir()
        for entry in plan:
            input_path = inputs / f"{entry.case.index:03d}.yaml"
            _write_resolved_benchmark(input_path, entry)
            child_path = temp / entry.relative_path
            run_single(
                RunRequest(
                    benchmark_source=input_path,
                    backend=request.backend,
                    seed=entry.case.seed,
                    output=child_path,
                )
            )
            bundle = read_bundle(child_path)
            if bundle.manifest.execution_hash != entry.execution_hash:
                raise SweepError(
                    f"{entry.relative_path}: child execution hash does not match plan"
                )
            if bundle.manifest.run_id != entry.run_id:
                raise SweepError(
                    f"{entry.relative_path}: child run ID does not match plan"
                )
        shutil.rmtree(inputs)
        manifest = _manifest_data(
            loaded=loaded,
            backend=request.backend,
            identity=identity,
            plan=plan,
            started_at=started_at,
            ended_at=_utc_now(),
        )
        (temp / "sweep_manifest.json").write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        aggregate_sweep(temp)
        temp.replace(output)
    except Exception as error:
        shutil.rmtree(temp, ignore_errors=True)
        if isinstance(error, SweepError):
            raise
        if isinstance(error, QNetBenchError):
            raise SweepError(f"sweep execution failed: {error}") from error
        raise SweepError(f"sweep execution failed: {error}") from error
    return output
