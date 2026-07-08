from datetime import UTC, datetime, timedelta

from duratypes.integrations.pydantic_graph import TimeoutGuard

if __name__ == "__main__":
    started_at = datetime.now(UTC) - timedelta(seconds=30)
    guard = TimeoutGuard(max_duration="10m")
    print(
        {
            "guard": guard.model_dump(),
            "expired": guard.expired(started_at),
        }
    )
