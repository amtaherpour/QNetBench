"""Canonical bundle failure and atomic-write tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from qnetbench.artifacts import read_bundle, write_complete_bundle
from qnetbench.artifacts import writer as artifact_writer
from qnetbench.errors import ArtifactError
from qnetbench.results import RunManifest

FIXTURES = Path("tests/fixtures/results")


def test_existing_destination_requires_explicit_overwrite(tmp_path: Path) -> None:
    source = read_bundle(FIXTURES / "complete_run")
    destination = tmp_path / "bundle"
    destination.mkdir()
    marker = destination / "keep.txt"
    marker.write_text("old", encoding="utf-8")
    with pytest.raises(ArtifactError, match="already exists"):
        write_complete_bundle(
            destination,
            source.benchmark,
            source.manifest,
            source.requests,
            source.metrics,
            source.summary,
        )
    assert marker.read_text(encoding="utf-8") == "old"
    write_complete_bundle(
        destination,
        source.benchmark,
        source.manifest,
        source.requests,
        source.metrics,
        source.summary,
        overwrite=True,
    )
    assert not marker.exists()
    assert read_bundle(destination).manifest == source.manifest


def test_invalid_write_leaves_no_complete_destination(tmp_path: Path) -> None:
    source = read_bundle(FIXTURES / "complete_run")
    data = source.manifest.model_dump(mode="json")
    data["benchmark_hash"] = "f" * 64
    bad_manifest = RunManifest.model_validate(data)
    destination = tmp_path / "invalid"
    with pytest.raises(ArtifactError, match="benchmark_hash"):
        write_complete_bundle(
            destination,
            source.benchmark,
            bad_manifest,
            source.requests,
            source.metrics,
            source.summary,
        )
    assert not destination.exists()
    assert not list(tmp_path.glob(".invalid.tmp-*"))


def test_finalization_failure_cleans_temporary_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = read_bundle(FIXTURES / "complete_run")
    destination = tmp_path / "finalize-failure"

    def fail_finalize(temp: Path, target: Path, overwrite: bool) -> None:
        raise OSError("synthetic rename failure")

    monkeypatch.setattr(artifact_writer, "_finalize", fail_finalize)
    with pytest.raises(OSError, match="synthetic rename failure"):
        write_complete_bundle(
            destination,
            source.benchmark,
            source.manifest,
            source.requests,
            source.metrics,
            source.summary,
        )
    assert not destination.exists()
    assert not list(tmp_path.glob(".finalize-failure.tmp-*"))


def test_malformed_jsonl_reports_file_and_line(tmp_path: Path) -> None:
    destination = tmp_path / "corrupt"
    source = FIXTURES / "complete_run"
    destination.mkdir()
    for name in ("benchmark.yaml", "run_manifest.json", "metrics.csv", "summary.json"):
        (destination / name).write_bytes((source / name).read_bytes())
    good_line = (source / "requests.jsonl").read_text(encoding="utf-8").splitlines()[0]
    (destination / "requests.jsonl").write_text(
        good_line + "\n{not valid json}\n",
        encoding="utf-8",
    )
    with pytest.raises(ArtifactError, match=r"requests\.jsonl:2"):
        read_bundle(destination)


def test_missing_required_complete_file_fails(tmp_path: Path) -> None:
    destination = tmp_path / "missing"
    source = FIXTURES / "complete_run"
    destination.mkdir()
    for name in (
        "benchmark.yaml",
        "run_manifest.json",
        "requests.jsonl",
        "summary.json",
    ):
        (destination / name).write_bytes((source / name).read_bytes())
    with pytest.raises(ArtifactError, match="metrics.csv"):
        read_bundle(destination)


def test_failed_run_rejects_standard_metrics(tmp_path: Path) -> None:
    destination = tmp_path / "bad-failed"
    source = FIXTURES / "failed_run"
    destination.mkdir()
    for path in source.iterdir():
        if path.is_file():
            (destination / path.name).write_bytes(path.read_bytes())
    (destination / "metrics.csv").write_text(
        "metric_id,status,value,unit,population_count,coverage_count\n",
        encoding="utf-8",
    )
    with pytest.raises(ArtifactError, match="failed run contains standard metrics"):
        read_bundle(destination)


def test_nonfinite_json_is_rejected(tmp_path: Path) -> None:
    destination = tmp_path / "nan"
    source = FIXTURES / "complete_run"
    destination.mkdir()
    for path in source.iterdir():
        if path.is_file():
            (destination / path.name).write_bytes(path.read_bytes())
    manifest = json.loads((destination / "run_manifest.json").read_text())
    manifest["measurement_end_s"] = float("nan")
    (destination / "run_manifest.json").write_text(
        json.dumps(manifest, allow_nan=True),
        encoding="utf-8",
    )
    with pytest.raises(ArtifactError, match="non-finite"):
        read_bundle(destination)
