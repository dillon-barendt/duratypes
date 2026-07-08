from datetime import UTC, datetime, timedelta

from duratypes.integrations.pydantic_graph import TimeoutGuard


def test_timeout_guard_not_expired() -> None:
    started_at = datetime.now(UTC)
    guard = TimeoutGuard(max_duration="10m")

    assert guard.expired(started_at, now=started_at) is False


def test_timeout_guard_expired() -> None:
    started_at = datetime.now(UTC)
    guard = TimeoutGuard(max_duration="10m", retry_delay="5s")

    assert guard.retry_delay == 5
    assert guard.expired(started_at, now=started_at + timedelta(minutes=10)) is True
