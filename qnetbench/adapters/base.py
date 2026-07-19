"""Backend adapter boundary for QNetBench."""

from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from qnetbench.errors import UnsupportedBenchmarkError
from qnetbench.results import RequestResult
from qnetbench.spec import BenchmarkSpec


@dataclass(frozen=True)
class BackendIdentity:
    """Stable adapter/backend identity recorded in run provenance."""

    adapter_name: str
    adapter_version: str
    backend_name: str
    backend_version: str | None


@dataclass(frozen=True)
class SupportReport:
    """Structured result of checking one benchmark against an adapter."""

    supported: bool
    reasons: tuple[str, ...]
    unsupported_paths: tuple[str, ...]
    warnings: tuple[str, ...]
    backend_identity: BackendIdentity

    def as_dict(self) -> dict[str, Any]:
        return {
            "supported": self.supported,
            "reasons": list(self.reasons),
            "unsupported_paths": list(self.unsupported_paths),
            "warnings": list(self.warnings),
            "backend_identity": {
                "adapter_name": self.backend_identity.adapter_name,
                "adapter_version": self.backend_identity.adapter_version,
                "backend_name": self.backend_identity.backend_name,
                "backend_version": self.backend_identity.backend_version,
            },
        }

    def digest(self) -> str:
        payload = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AdapterRun:
    """Canonical in-memory output produced by one adapter execution."""

    requests: tuple[RequestResult, ...]
    measurement_start_s: float
    measurement_end_s: float
    backend_identity: BackendIdentity
    warnings: tuple[str, ...] = ()


class Adapter(ABC):
    """Abstract backend boundary; adapters never calculate metrics or write bundles."""

    @property
    @abstractmethod
    def identity(self) -> BackendIdentity:
        """Return stable adapter and backend identity."""

    @abstractmethod
    def check_support(self, benchmark: BenchmarkSpec) -> SupportReport:
        """Inspect a validated benchmark without executing it."""

    @abstractmethod
    def _run_supported(
        self,
        benchmark: BenchmarkSpec,
        *,
        benchmark_hash: str,
        seed: int,
    ) -> AdapterRun:
        """Execute a benchmark already confirmed as supported."""

    def run(
        self,
        benchmark: BenchmarkSpec,
        *,
        benchmark_hash: str,
        seed: int,
    ) -> AdapterRun:
        """Check support, then execute or raise a typed pre-execution failure."""
        report = self.check_support(benchmark)
        if not report.supported:
            details = "; ".join(
                f"{path}: {reason}"
                for path, reason in zip(
                    report.unsupported_paths,
                    report.reasons,
                    strict=False,
                )
            )
            raise UnsupportedBenchmarkError(
                details or "benchmark is not supported by this adapter",
                report=report,
            )
        return self._run_supported(
            benchmark,
            benchmark_hash=benchmark_hash,
            seed=seed,
        )
