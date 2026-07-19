"""Checkpoint 0 package import tests."""

import qnetbench


def test_package_version() -> None:
    """The package imports and exposes the Checkpoint 0 development version."""
    assert qnetbench.__version__ == "0.0.0.dev0"
