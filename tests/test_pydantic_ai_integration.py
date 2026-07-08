from datetime import UTC, datetime, timedelta

from duratypes.integrations.pydantic_ai import RunBudget, remaining_budget_seconds


def test_run_budget_parses_duration_values() -> None:
    budget = RunBudget(max_duration="2m", retry_delay="5s")

    assert budget.max_duration == 120
    assert budget.retry_delay == 5
    assert budget.max_retries == 3

    default_budget = RunBudget()
    assert default_budget.max_duration == 120
    assert default_budget.retry_delay == 5


def test_remaining_budget_seconds() -> None:
    started_at = datetime.now(UTC)
    budget = RunBudget(max_duration="2m", retry_delay="5s")
    now = started_at + timedelta(seconds=30)

    assert remaining_budget_seconds(started_at, budget, now=now) == 90
