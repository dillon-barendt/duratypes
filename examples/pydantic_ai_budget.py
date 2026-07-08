from datetime import UTC, datetime, timedelta

from duratypes.integrations.pydantic_ai import RunBudget, remaining_budget_seconds

if __name__ == "__main__":
    started_at = datetime.now(UTC) - timedelta(seconds=30)
    budget = RunBudget(max_duration="2m", retry_delay="5s", max_retries=3)
    print(
        {
            "budget": budget.model_dump(),
            "remaining_seconds": remaining_budget_seconds(started_at, budget),
        }
    )
