"""FastAPI helpers for duration query, header, and path values."""

from importlib import import_module
from typing import Any

from duratypes import Duration

DurationQuery = Duration
DurationHeader = Duration
DurationPath = Duration

__all__ = [
    "DurationHeader",
    "DurationPath",
    "DurationQuery",
    "duration_header",
    "duration_path",
    "duration_query",
]


def _fastapi_param(name: str, default: object, **kwargs: Any) -> Any:
    try:
        fastapi = import_module("fastapi")
    except ImportError as exc:
        raise ImportError(
            "FastAPI helpers require FastAPI. Install with `pip install duratypes[fastapi]`."
        ) from exc
    return getattr(fastapi, name)(default, **kwargs)


def duration_query(default: object = ..., **kwargs: Any) -> Any:
    """Return a FastAPI ``Query`` default for a ``Duration`` field."""
    return _fastapi_param("Query", default, **kwargs)


def duration_header(default: object = ..., **kwargs: Any) -> Any:
    """Return a FastAPI ``Header`` default for a ``Duration`` field."""
    return _fastapi_param("Header", default, **kwargs)


def duration_path(default: object = ..., **kwargs: Any) -> Any:
    """Return a FastAPI ``Path`` default for a ``Duration`` field."""
    return _fastapi_param("Path", default, **kwargs)
