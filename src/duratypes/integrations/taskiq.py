"""Dependency-free helpers for Taskiq-style timeout and retry values."""

from duratypes import DurationInput, InvalidValueError, to_milliseconds, to_seconds

__all__ = ["retry_delay", "schedule_every", "task_timeout"]


def _require_positive_seconds(value: DurationInput, label: str) -> int:
    seconds = to_seconds(value)
    if seconds <= 0:
        raise InvalidValueError(f"{label} must be greater than 0 seconds")
    return seconds


def _require_non_negative_seconds(value: DurationInput, label: str) -> int:
    seconds = to_seconds(value)
    if seconds < 0:
        raise InvalidValueError(f"{label} must be greater than or equal to 0 seconds")
    return seconds


def task_timeout(value: DurationInput) -> int:
    """Convert a duration into integer seconds for task timeout configuration."""
    return _require_positive_seconds(value, "task timeout")


def retry_delay(value: DurationInput) -> int:
    """Convert a duration into integer seconds for retry delay configuration."""
    return _require_non_negative_seconds(value, "retry delay")


def schedule_every(value: DurationInput) -> dict[str, object]:
    """Return a small schedule metadata payload with seconds and milliseconds."""
    seconds = _require_positive_seconds(value, "schedule interval")
    return {
        "every_seconds": seconds,
        "every_milliseconds": to_milliseconds(value),
    }
