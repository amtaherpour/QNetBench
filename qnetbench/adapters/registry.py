"""Adapter factory registry."""

from __future__ import annotations

from collections.abc import Callable

from qnetbench.adapters.base import Adapter
from qnetbench.errors import AdapterError

AdapterFactory = Callable[[], Adapter]
_FACTORIES: dict[str, AdapterFactory] = {}


def register_adapter(
    name: str, factory: AdapterFactory, *, replace: bool = False
) -> None:
    normalized = name.strip().lower()
    if not normalized:
        raise ValueError("adapter name must not be empty")
    if normalized in _FACTORIES and not replace:
        raise AdapterError(f"adapter {normalized!r} is already registered")
    _FACTORIES[normalized] = factory


def available_adapters() -> tuple[str, ...]:
    return tuple(sorted(_FACTORIES))


def get_adapter(name: str) -> Adapter:
    normalized = name.strip().lower()
    try:
        factory = _FACTORIES[normalized]
    except KeyError as error:
        available = ", ".join(available_adapters()) or "none"
        raise AdapterError(
            f"unknown adapter {name!r}; available adapters: {available}"
        ) from error
    return factory()
