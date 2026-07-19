"""Canonical bundle read/write round-trip tests."""

from __future__ import annotations

from pathlib import Path

from qnetbench.artifacts import read_bundle, write_complete_bundle, write_failed_bundle

FIXTURES = Path("tests/fixtures/results")


def test_checked_in_complete_fixture_validates() -> None:
    bundle = read_bundle(FIXTURES / "complete_run")
    assert bundle.manifest.status == "complete"
    assert len(bundle.requests) == 2
    assert len(bundle.metrics) == 8
    assert bundle.summary is not None
    assert bundle.error is None


def test_checked_in_failed_fixture_validates() -> None:
    bundle = read_bundle(FIXTURES / "failed_run")
    assert bundle.manifest.status == "failed"
    assert bundle.error is not None
    assert bundle.metrics == ()
    assert bundle.summary is None


def test_complete_bundle_round_trip(tmp_path: Path) -> None:
    source = read_bundle(FIXTURES / "complete_run")
    destination = tmp_path / "complete"
    write_complete_bundle(
        destination,
        source.benchmark,
        source.manifest,
        source.requests,
        source.metrics,
        source.summary,
    )
    restored = read_bundle(destination)
    assert restored.benchmark == source.benchmark
    assert restored.manifest == source.manifest
    assert restored.requests == source.requests
    assert restored.metrics == source.metrics
    assert restored.summary == source.summary


def test_failed_bundle_round_trip(tmp_path: Path) -> None:
    source = read_bundle(FIXTURES / "failed_run")
    destination = tmp_path / "failed"
    write_failed_bundle(
        destination,
        source.benchmark,
        source.manifest,
        source.error,
        requests=source.requests,
    )
    restored = read_bundle(destination)
    assert restored.benchmark == source.benchmark
    assert restored.manifest == source.manifest
    assert restored.error == source.error


def test_optional_events_and_raw_are_ignored() -> None:
    bundle = read_bundle(FIXTURES / "complete_run")
    assert (bundle.path / "events.jsonl").exists()
    assert (bundle.path / "raw" / "backend.txt").exists()
