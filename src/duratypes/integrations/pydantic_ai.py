"""Pydantic AI-adjacent duration helpers without a runtime dependency."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from duratypes import NonNegativeDuration, PositiveDuration, parse_duration

__all__ = ["RunBudget", "remaining_budget_seconds"]


class RunBudget(BaseModel):
    """Runtime budget for an agent or tool execution."""

    max_duration: PositiveDuration = Field(default_factory=lambda: parse_duration("2m"))
    retry_delay: NonNegativeDuration = Field(
        default_factory=lambda: parse_duration("5s")
    )
    max_retries: int = Field(default=3, ge=0)


def _now_like(started_at: datetime) -> datetime:
    if started_at.tzinfo is None:
        return datetime.now()
    return datetime.now(UTC)


def remaining_budget_seconds(
    started_at: datetime,
    budget: RunBudget,
    now: datetime | None = None,
) -> int:
    """Return remaining integer seconds in a run budget."""
    current = now if now is not None else _now_like(started_at)
    elapsed = max(int((current - started_at).total_seconds()), 0)
    return max(budget.max_duration - elapsed, 0)
