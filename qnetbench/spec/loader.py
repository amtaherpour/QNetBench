"""Safe YAML/JSON loading for BenchmarkSpec v0.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NoReturn

import yaml
from pydantic import ValidationError

from qnetbench.errors import ConfigError
from qnetbench.spec.models import BenchmarkSpec


def _reject_json_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON constant {value!r} is not allowed")


def _format_location(location: tuple[int | str, ...]) -> str:
    if not location:
        return "benchmark"
    result = ""
    for part in location:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += ("." if result else "") + part
    return result


def _format_validation_error(error: ValidationError) -> str:
    details: list[str] = []
    for item in error.errors(include_url=False):
        location = _format_location(tuple(item["loc"]))
        details.append(f"{location}: {item['msg']}")
    return "invalid BenchmarkSpec v0.1: " + "; ".join(details)


def _load_document(path: Path, text: str) -> Any:
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            return json.loads(text, parse_constant=_reject_json_constant)
        if suffix in {".yaml", ".yml"}:
            return yaml.safe_load(text)
    except (json.JSONDecodeError, ValueError, yaml.YAMLError) as error:
        raise ConfigError(f"could not parse benchmark: {error}", source=path) from error
    raise ConfigError(
        "unsupported benchmark format; expected .yaml, .yml, or .json",
        source=path,
    )


def load_benchmark(source: str | Path) -> BenchmarkSpec:
    """Load one benchmark file or raise a human-readable ``ConfigError``."""
    path = Path(source)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ConfigError(f"could not read benchmark: {error}", source=path) from error

    document = _load_document(path, text)
    if not isinstance(document, dict):
        raise ConfigError("benchmark document must be a mapping", source=path)

    try:
        return BenchmarkSpec.model_validate(document)
    except ValidationError as error:
        raise ConfigError(_format_validation_error(error), source=path) from error
