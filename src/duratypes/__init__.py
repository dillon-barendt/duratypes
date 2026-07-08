"""
duratypes - Typed duration utilities for Python and Pydantic.
Supports strings like '30s', '5m', '1h' and normalizes them to integer seconds.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("duratypes")
except PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Dillon Barendt"
__email__ = "dillon.barendt@ticket-vision.com"

from .core import (
    Duration,
    DurationAdapter,
    DurationError,
    DurationInput,
    DurationRange,
    Hours,
    InvalidFormatError,
    InvalidTypeError,
    InvalidValueError,
    Milliseconds,
    Minutes,
    NonNegativeDuration,
    PositiveDuration,
    Seconds,
    format_duration,
    parse_duration,
    to_iso8601,
    to_milliseconds,
    to_seconds,
    to_timedelta,
)

__all__ = [
    "Duration",
    "DurationAdapter",
    "DurationError",
    "DurationInput",
    "DurationRange",
    "Hours",
    "InvalidFormatError",
    "InvalidTypeError",
    "InvalidValueError",
    "Milliseconds",
    "Minutes",
    "NonNegativeDuration",
    "PositiveDuration",
    "Seconds",
    "format_duration",
    "parse_duration",
    "to_iso8601",
    "to_milliseconds",
    "to_seconds",
    "to_timedelta",
]
