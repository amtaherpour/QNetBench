from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict:
    value = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_open_targets_are_pinned_sequence_and_q2ns() -> None:
    portfolio = _load("simulators/portfolio_v1.yaml")
    assert portfolio["decision_status"] == "frozen"
    targets = portfolio["mandatory_open_targets"]
    assert [target["simulator_id"] for target in targets] == ["sequence", "q2ns"]
    assert [target["selected_source_commit"] for target in targets] == [
        "ffd7c837f932c7bdc9450cd211aaf75b4d6a99a5",
        "f22ba28f437099ba3cf9956ca332ba5ce8bb14fd",
    ]
    assert all(target["public_ci"] is True for target in targets)
    assert len({target["architecture_family"] for target in targets}) == 2
    assert portfolio["core_oracle"]["physical_claims_allowed"] is False


def test_probe_evidence_matches_frozen_portfolio() -> None:
    manifest = _load("research/evidence/probe_manifest.json")
    assert set(manifest["probes"]) == {"sequence", "q2ns", "quisp", "netsquid"}
    assert all(probe["status"] == "success" for probe in manifest["probes"].values())
    q2ns = _load("research/evidence/q2ns_probe.json")
    assert q2ns["q2ns_commit"] == "f22ba28f437099ba3cf9956ca332ba5ce8bb14fd"
    assert q2ns["ns3_commit"] == "e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f"
    assert q2ns["build_completed"] is True
    assert q2ns["example_completed"] is True


def test_optional_lanes_do_not_block_open_core() -> None:
    portfolio = _load("simulators/portfolio_v1.yaml")
    reserve = portfolio["qualification_reserve"][0]
    assert reserve["simulator_id"] == "quisp"
    assert reserve["selected_source_commit"] == (
        "2530200c5aa8f43a6f1471c16b8abb98c4b7ee2c"
    )
    netsquid = portfolio["optional_credentialed"][0]
    assert netsquid["simulator_id"] == "netsquid"
    assert netsquid["public_ci"] is False
    assert portfolio["fallback_policy"]["netsquid_unavailable"] == (
        "continue_open_paper_core_without_blocking"
    )


def test_conformance_preserves_v01() -> None:
    conformance = _load("simulators/conformance_v1.yaml")
    policy = conformance["comparison_policy"]
    assert policy["require_numeric_equality_across_simulators"] is False
    assert policy["require_identical_benchmark_identity"] is True
    assert policy["require_common_metric_definitions"] is True
    assert policy["prohibit_mock_as_physical_reference"] is True
    assert conformance["versioning_policy"]["preserve_v0_1"] is True


def test_checkpoint_85_has_no_production_real_adapter() -> None:
    directory = ROOT / "qnetbench" / "adapters"
    names = ("sequence.py", "q2ns.py", "quisp.py", "netsquid.py")
    assert not any((directory / name).exists() for name in names)


def test_paper_roadmap_is_finite() -> None:
    roadmap = (ROOT / "docs/planning/QNetBench_Paper_Track_Roadmap_v1_0.md").read_text(
        encoding="utf-8"
    )
    for checkpoint in (9, 10, 11, 12):
        assert f"Checkpoint {checkpoint}" in roadmap
    assert "Checkpoint 13" not in roadmap
    assert "completed Checkpoints 0–8" in roadmap
    assert "Tests are never weakened" in roadmap
