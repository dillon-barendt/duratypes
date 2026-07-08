import pytest
from pydantic import BaseModel, ValidationError

from duratypes import (
    DurationRange,
    Milliseconds,
    NonNegativeDuration,
    PositiveDuration,
)


def test_positive_duration_parses_and_rejects_zero() -> None:
    class Settings(BaseModel):
        timeout: PositiveDuration

    assert Settings(timeout="30s").timeout == 30

    with pytest.raises(ValidationError):
        Settings(timeout="0s")


def test_non_negative_duration_accepts_zero_and_rejects_negative() -> None:
    class Settings(BaseModel):
        retry_delay: NonNegativeDuration

    assert Settings(retry_delay="0s").retry_delay == 0

    with pytest.raises(ValidationError):
        Settings(retry_delay="-1s")


def test_milliseconds_normalizes_to_integer_milliseconds() -> None:
    class Settings(BaseModel):
        timeout: Milliseconds

    assert Settings(timeout="1.5s").timeout == 1500
    assert Settings(timeout=2).timeout == 2000


def test_duration_range_validates_bounds() -> None:
    window = DurationRange(min="5s", max="1m")

    assert window.min == 5
    assert window.max == 60

    with pytest.raises(ValidationError):
        DurationRange(min="2m", max="1m")
