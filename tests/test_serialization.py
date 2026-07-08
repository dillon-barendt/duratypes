from datetime import timedelta

from duratypes import to_iso8601, to_milliseconds, to_seconds, to_timedelta


def test_to_seconds_uses_normalized_integer_seconds() -> None:
    assert to_seconds("1h30m") == 5400
    assert to_seconds("1.9s") == 1


def test_to_milliseconds_preserves_fractional_seconds() -> None:
    assert to_milliseconds("1.5s") == 1500
    assert to_milliseconds(2.25) == 2250


def test_to_timedelta_preserves_fractional_seconds() -> None:
    assert to_timedelta("5m") == timedelta(minutes=5)
    assert to_timedelta("1.5s") == timedelta(seconds=1.5)


def test_to_iso8601_uses_integer_seconds() -> None:
    assert to_iso8601("1h30m") == "PT1H30M"
    assert to_iso8601("1d2h") == "P1DT2H"
    assert to_iso8601("0s") == "PT0S"
    assert to_iso8601("-30s") == "-PT30S"
