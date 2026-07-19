"""Deterministic BenchmarkSpec normalization and hashing."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from qnetbench.spec.models import BenchmarkSpec


def _normalize_number(value: Any) -> Any:
    """Normalize negative zero and recursively copy JSON-compatible values."""
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("canonical JSON cannot contain a non-finite number")
        return 0.0 if value == 0.0 else value
    if isinstance(value, dict):
        return {key: _normalize_number(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_number(item) for item in value]
    return value


def canonical_data(spec: BenchmarkSpec) -> dict[str, Any]:
    """Return the normalized JSON-compatible benchmark mapping."""
    data = spec.model_dump(mode="json")
    normalized = _normalize_number(data)
    if not isinstance(normalized, dict):  # pragma: no cover - defensive only
        raise TypeError("BenchmarkSpec normalization did not produce a mapping")
    return normalized


def canonical_json(spec: BenchmarkSpec) -> str:
    """Serialize a benchmark using the frozen compact canonical JSON procedure."""
    return json.dumps(
        canonical_data(spec),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def benchmark_hash(spec: BenchmarkSpec) -> str:
    """Return lowercase SHA-256 over UTF-8 canonical JSON bytes."""
    return hashlib.sha256(canonical_json(spec).encode("utf-8")).hexdigest()
