import pytest

from duratypes import InvalidValueError
from duratypes.integrations.taskiq import retry_delay, schedule_every, task_timeout


def test_taskiq_helpers_return_runtime_primitives() -> None:
    assert task_timeout("2m") == 120
    assert retry_delay("30s") == 30
    assert schedule_every("5m") == {
        "every_seconds": 300,
        "every_milliseconds": 300000,
    }


def test_taskiq_helpers_reject_invalid_bounds() -> None:
    with pytest.raises(InvalidValueError):
        task_timeout("0s")

    with pytest.raises(InvalidValueError):
        retry_delay("-1s")
