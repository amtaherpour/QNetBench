"""Adapter-neutral orchestration for one QNetBench execution."""

from __future__ import annotations

import hashlib
import json
import platform
import traceback
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from qnetbench import __version__
from qnetbench.adapters import AdapterRun, BackendIdentity, SupportReport, get_adapter
from qnetbench.artifacts import write_complete_bundle, write_failed_bundle
from qnetbench.errors import (
    AdapterError,
    ArtifactError,
    MetricComputationError,
    RunError,
    UnsupportedBenchmarkError,
)
from qnetbench.metrics import compute_metrics
from qnetbench.results import ErrorRecord, RunManifest, Summary
from qnetbench.spec import BenchmarkSpec, benchmark_hash, load_benchmark


@dataclass(frozen=True)
class RunRequest:
    """Execution concerns kept outside the backend-independent benchmark."""

    benchmark_source: Path
    backend: str
    seed: int
    output: Path
    overwrite: bool = False


def execution_hash(
    benchmark_digest: str,
    identity: BackendIdentity,
    seed: int,
) -> str:
    """Hash scientific execution inputs; timestamps and output paths are excluded."""
    payload = json.dumps(
        {
            "adapter_name": identity.adapter_name,
            "adapter_version": identity.adapter_version,
            "backend_name": identity.backend_name,
            "backend_version": identity.backend_version,
            "benchmark_hash": benchmark_digest,
            "execution_options": {},
            "seed": seed,
        },
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def make_run_id(
    benchmark_id: str,
    backend_name: str,
    seed: int,
    execution_digest: str,
) -> str:
    """Create a readable run ID without treating it as the source of truth."""
    return f"{benchmark_id}-{backend_name}-{seed}-{execution_digest[:8]}"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _warnings(
    report: SupportReport, adapter_run: AdapterRun | None = None
) -> tuple[str, ...]:
    values = [*report.warnings]
    if adapter_run is not None:
        values.extend(adapter_run.warnings)
    return tuple(dict.fromkeys(values))


def _manifest(
    *,
    benchmark: BenchmarkSpec,
    benchmark_digest: str,
    execution_digest: str,
    identity: BackendIdentity,
    seed: int,
    status: str,
    started_at: str,
    ended_at: str,
    measurement_start_s: float,
    measurement_end_s: float,
    written_request_count: int,
    warnings: tuple[str, ...],
    support_digest: str,
) -> RunManifest:
    return RunManifest(
        result_schema_version="0.1",
        run_id=make_run_id(
            benchmark.benchmark_id,
            identity.backend_name,
            seed,
            execution_digest,
        ),
        benchmark_id=benchmark.benchmark_id,
        benchmark_hash=benchmark_digest,
        execution_hash=execution_digest,
        qnetbench_version=__version__,
        adapter_name=identity.adapter_name,
        adapter_version=identity.adapter_version,
        backend_name=identity.backend_name,
        backend_version=identity.backend_version,
        seed=seed,
        status=status,
        started_at_utc=started_at,
        ended_at_utc=ended_at,
        measurement_start_s=measurement_start_s,
        measurement_end_s=measurement_end_s,
        expected_request_count=benchmark.workload.request_count,
        written_request_count=written_request_count,
        python_version=platform.python_version(),
        platform=platform.platform(),
        warnings=warnings,
        support_report_digest=support_digest,
    )


def _error_record(error: BaseException, stage: str) -> ErrorRecord:
    rendered = traceback.format_exc()
    if rendered.strip() == "NoneType: None":
        rendered = f"{type(error).__name__}: {error}"
    return ErrorRecord(
        error_schema_version="0.1",
        exception_type=type(error).__name__,
        message=str(error) or type(error).__name__,
        stage=stage,
        traceback=rendered,
    )


def _write_failure(
    request: RunRequest,
    benchmark: BenchmarkSpec,
    benchmark_digest: str,
    report: SupportReport,
    *,
    execution_digest: str,
    started_at: str,
    error: BaseException,
    stage: str,
    adapter_run: AdapterRun | None = None,
) -> Path:
    ended_at = _utc_now()
    written = 0 if adapter_run is None else len(adapter_run.requests)
    measurement_start = benchmark.workload.batch_start_s
    measurement_end = measurement_start
    requests = ()
    if adapter_run is not None:
        measurement_start = adapter_run.measurement_start_s
        measurement_end = adapter_run.measurement_end_s
        requests = adapter_run.requests
    manifest = _manifest(
        benchmark=benchmark,
        benchmark_digest=benchmark_digest,
        execution_digest=execution_digest,
        identity=report.backend_identity,
        seed=request.seed,
        status="failed",
        started_at=started_at,
        ended_at=ended_at,
        measurement_start_s=measurement_start,
        measurement_end_s=measurement_end,
        written_request_count=written,
        warnings=_warnings(report, adapter_run),
        support_digest=report.digest(),
    )
    write_failed_bundle(
        request.output,
        benchmark,
        manifest,
        _error_record(error, stage),
        requests=requests,
        overwrite=request.overwrite,
    )
    return request.output


def run_single(request: RunRequest) -> Path:
    """Execute one validated benchmark and write one canonical result bundle."""
    if request.output.exists() and not request.overwrite:
        raise ArtifactError(
            f"{request.output}: destination already exists; use overwrite explicitly"
        )

    benchmark = load_benchmark(request.benchmark_source)
    benchmark_digest = benchmark_hash(benchmark)
    adapter = get_adapter(request.backend)
    report = adapter.check_support(benchmark)
    execution_digest = execution_hash(
        benchmark_digest,
        report.backend_identity,
        request.seed,
    )
    started_at = _utc_now()

    if not report.supported:
        details = "; ".join(
            f"{path}: {reason}"
            for path, reason in zip(
                report.unsupported_paths,
                report.reasons,
                strict=False,
            )
        )
        error = UnsupportedBenchmarkError(
            details or "benchmark is unsupported",
            report=report,
        )
        output = _write_failure(
            request,
            benchmark,
            benchmark_digest,
            report,
            execution_digest=execution_digest,
            started_at=started_at,
            error=error,
            stage="support_check",
        )
        raise RunError(str(error), output=output) from error

    try:
        adapter_run = adapter.run(
            benchmark,
            benchmark_hash=benchmark_digest,
            seed=request.seed,
        )
    except Exception as error:
        output = _write_failure(
            request,
            benchmark,
            benchmark_digest,
            report,
            execution_digest=execution_digest,
            started_at=started_at,
            error=error,
            stage="execution",
        )
        raise RunError(str(error), output=output) from error

    failure: BaseException | None = None
    stage = "normalization"
    try:
        if adapter_run.backend_identity != report.backend_identity:
            raise AdapterError(
                "adapter execution identity does not match its support report"
            )
        provisional_manifest = _manifest(
            benchmark=benchmark,
            benchmark_digest=benchmark_digest,
            execution_digest=execution_digest,
            identity=adapter_run.backend_identity,
            seed=request.seed,
            status="complete",
            started_at=started_at,
            ended_at=_utc_now(),
            measurement_start_s=adapter_run.measurement_start_s,
            measurement_end_s=adapter_run.measurement_end_s,
            written_request_count=len(adapter_run.requests),
            warnings=_warnings(report, adapter_run),
            support_digest=report.digest(),
        )
        metrics = compute_metrics(
            provisional_manifest,
            adapter_run.requests,
            benchmark.requested_metrics,
        )
        summary = Summary(
            result_schema_version="0.1",
            run_id=provisional_manifest.run_id,
            status="complete",
            metrics={row.metric_id: row.value for row in metrics},
        )
        return write_complete_bundle(
            request.output,
            benchmark,
            provisional_manifest,
            adapter_run.requests,
            metrics,
            summary,
            overwrite=request.overwrite,
        )
    except MetricComputationError as caught:
        failure = caught
        stage = "metrics"
    except (AdapterError, ValueError) as caught:
        failure = caught
    except ArtifactError:
        raise
    except Exception as caught:
        failure = caught

    assert failure is not None
    output = _write_failure(
        request,
        benchmark,
        benchmark_digest,
        report,
        execution_digest=execution_digest,
        started_at=started_at,
        error=failure,
        stage=stage,
        adapter_run=adapter_run,
    )
    raise RunError(str(failure), output=output) from failure
