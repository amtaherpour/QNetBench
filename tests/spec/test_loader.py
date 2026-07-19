"""Safe benchmark loading tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from qnetbench.errors import ConfigError
from qnetbench.spec import load_benchmark

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "spec"


def test_yaml_and_json_load_to_equivalent_models() -> None:
    yaml_spec = load_benchmark(FIXTURES / "valid_equivalent.yaml")
    json_spec = load_benchmark(FIXTURES / "valid_equivalent.json")
    assert yaml_spec == json_spec


def test_unknown_field_reports_human_readable_path() -> None:
    with pytest.raises(ConfigError) as captured:
        load_benchmark(FIXTURES / "invalid_unknown_field.yaml")
    message = str(captured.value)
    assert "backend" in message
    assert "Extra inputs are not permitted" in message


def test_unsafe_yaml_constructor_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "unsafe.yaml"
    source.write_text(
        "!!python/object/apply:os.system ['echo unsafe']\n", encoding="utf-8"
    )
    with pytest.raises(ConfigError, match="could not parse benchmark"):
        load_benchmark(source)


def test_non_finite_json_constant_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "invalid.json"
    source.write_text('{"value": NaN}', encoding="utf-8")
    with pytest.raises(ConfigError, match="non-finite JSON constant"):
        load_benchmark(source)


def test_non_mapping_document_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "list.yaml"
    source.write_text("- one\n- two\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="must be a mapping"):
        load_benchmark(source)


def test_unsupported_extension_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "benchmark.txt"
    source.write_text("{}", encoding="utf-8")
    with pytest.raises(ConfigError, match="unsupported benchmark format"):
        load_benchmark(source)
