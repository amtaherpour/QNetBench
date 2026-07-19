"""QNetBench public error types."""

from __future__ import annotations

from pathlib import Path


class QNetBenchError(Exception):
    """Base class for expected QNetBench failures."""


class ConfigError(QNetBenchError):
    """Raised when a benchmark source cannot be parsed or validated."""

    def __init__(self, message: str, *, source: str | Path | None = None) -> None:
        self.source = None if source is None else Path(source)
        if self.source is not None:
            message = f"{self.source}: {message}"
        super().__init__(message)


class ResultValidationError(QNetBenchError):
    """Raised when canonical result data violates the frozen contract."""


class ArtifactError(QNetBenchError):
    """Raised when a result bundle cannot be safely read or written."""
