"""Backend adapters and registry."""

from qnetbench.adapters.base import Adapter, AdapterRun, BackendIdentity, SupportReport
from qnetbench.adapters.mock import MOCK_ALGORITHM_VERSION, MockAdapter
from qnetbench.adapters.registry import (
    available_adapters,
    get_adapter,
    register_adapter,
)

register_adapter("mock", MockAdapter, replace=True)

__all__ = [
    "Adapter",
    "AdapterRun",
    "BackendIdentity",
    "MOCK_ALGORITHM_VERSION",
    "MockAdapter",
    "SupportReport",
    "available_adapters",
    "get_adapter",
    "register_adapter",
]
