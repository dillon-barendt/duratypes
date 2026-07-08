"""Pydantic Graph-adjacent timeout guards without a runtime dependency."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from duratypes import NonNegativeDuration, PositiveDuration, parse_duration

__all__ = ["TimeoutGuard"]


def _now_like(started_at: datetime) -> datetime:
    if started_at.tzinfo is None:
        return datetime.now()
    return datetime.now(UTC)


class TimeoutGuard(BaseModel):
    """Reusable timeout and retry guard for graph-style workflow steps."""

    max_duration: PositiveDuration
    retry_delay: NonNegativeDuration = Field(
        default_factory=lambda: parse_duration("0s")
    )

    def expired(self, started_at: datetime, now: datetime | None = None) -> bool:
        current = now if now is not None else _now_like(started_at)
        return (current - started_at).total_seconds() >= self.max_duration
