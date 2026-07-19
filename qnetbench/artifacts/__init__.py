"""Canonical result bundle I/O API."""

from qnetbench.artifacts.reader import RunBundle, read_bundle
from qnetbench.artifacts.writer import write_complete_bundle, write_failed_bundle

__all__ = [
    "RunBundle",
    "read_bundle",
    "write_complete_bundle",
    "write_failed_bundle",
]
