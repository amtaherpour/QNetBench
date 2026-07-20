from __future__ import annotations

from pathlib import Path

import pytest

from qnetbench.adapters import BackendIdentity
from qnetbench.errors import SweepError
from qnetbench.runners import build_sweep_plan
from qnetbench.sweeps import LoadedSweep, SweepSpec, expand_sweep, load_sweep

SWEEP = Path("sweeps/v0_1/link_loss_small.yaml")
EXPECTED_EXECUTION_HASHES = (
    "361ed58c3260d8e9fd401024dad1becdc7c2a834463e66d3a5b1b8ef68aba1f4",
    "c03a594a37edf5ccfa94b664cdb2fa1a25b0f9396c710742cf42a7964d058051",
    "3a43f5107fa08bc8fbdb1241ebc1fc0be230f8dc6065a0d5697f9fe68e8e9fa4",
    "fb8cdcf0157ab3e943d22f6dd8654008e4f1f9ce6b2337411420f51e87272c60",
    "202bf5fc20daaebc66b8ede018f18fef9e3fcab85395c0d72062187fa2eb6d81",
    "161e749e23a642aa0145e244ede10558408327105a4b120553935534c10a1984",
    "3f7d9e29ab2d6c6c0e0a78e05f69240a56d57c90b8b7f6b3bc318d0d83997b7a",
    "66386b6b6ce20237477c179e62c5bcf373df3ca81647cb1d014b567b0933d2e4",
    "71c7adb7910f7c6878da3cb80c9482859d7db8824fa20626579f2c11ff28c9b5",
)


def test_checked_sweep_expands_deterministically_to_nine_unique_runs() -> None:
    loaded = load_sweep(SWEEP)
    cases = expand_sweep(loaded)
    assert len(cases) == 9
    assert [case.seed for case in cases] == [1, 2, 3] * 3
    assert [case.parameter_map for case in cases] == [
        {"physical_profile.fiber_attenuation_db_per_km": value}
        for value in (0.1, 0.2, 0.3)
        for _ in range(3)
    ]
    plan = build_sweep_plan(loaded, backend="mock")
    assert tuple(entry.execution_hash for entry in plan) == EXPECTED_EXECUTION_HASHES
    assert len({entry.execution_hash for entry in plan}) == 9


def test_axis_paths_sort_lexically_but_values_and_seeds_keep_source_order() -> None:
    loaded = load_sweep(SWEEP)
    data = loaded.spec.model_dump(mode="json")
    data["axes"] = [
        {"path": "workload.request_count", "values": [4, 2]},
        {
            "path": "physical_profile.fiber_attenuation_db_per_km",
            "values": [0.3, 0.1],
        },
    ]
    data["seeds"] = [9, 7]
    spec = SweepSpec.model_validate(data)
    cases = expand_sweep(LoadedSweep(source=loaded.source, spec=spec))
    assert cases[0].parameters == (
        ("physical_profile.fiber_attenuation_db_per_km", 0.3),
        ("workload.request_count", 4),
    )
    assert [case.seed for case in cases[:2]] == [9, 7]
    assert cases[2].parameter_map["workload.request_count"] == 2


def test_more_than_one_hundred_runs_is_rejected_before_execution() -> None:
    loaded = load_sweep(SWEEP)
    data = loaded.spec.model_dump(mode="json")
    data["axes"] = [
        {
            "path": "workload.request_count",
            "values": list(range(1, 12)),
        }
    ]
    data["seeds"] = list(range(10))
    oversized = LoadedSweep(
        source=loaded.source,
        spec=SweepSpec.model_validate(data),
    )
    with pytest.raises(SweepError, match="110 runs"):
        expand_sweep(oversized)


def test_backend_identity_used_by_plan_is_stable() -> None:
    identity = BackendIdentity("mock", "0.1", "mock", "1.0")
    plan = build_sweep_plan(load_sweep(SWEEP), backend=identity.backend_name)
    assert plan[0].run_id.endswith(plan[0].execution_hash[:8])
