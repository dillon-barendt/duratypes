"""Broker-neutral header helpers for message stream duration metadata."""

from duratypes import DurationInput, InvalidValueError, to_milliseconds, to_seconds

__all__ = ["message_ttl_headers", "retry_headers"]


def _require_non_negative_milliseconds(value: DurationInput, label: str) -> int:
    milliseconds = to_milliseconds(value)
    if milliseconds < 0:
        raise InvalidValueError(f"{label} must be greater than or equal to 0")
    return milliseconds


def message_ttl_headers(ttl: DurationInput) -> dict[str, str]:
    """Return broker-neutral message TTL headers using millisecond precision."""
    return {"x-message-ttl-ms": str(_require_non_negative_milliseconds(ttl, "ttl"))}


def retry_headers(retry_after: DurationInput) -> dict[str, str]:
    """Return broker-neutral retry headers in seconds and milliseconds."""
    milliseconds = _require_non_negative_milliseconds(retry_after, "retry_after")
    return {
        "retry-after": str(to_seconds(retry_after)),
        "x-retry-after-ms": str(milliseconds),
    }
