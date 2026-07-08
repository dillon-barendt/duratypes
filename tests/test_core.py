import math

import pytest
from hypothesis import given, strategies as st

from duratypes import (
    DurationAdapter,
    DurationError,
    InvalidFormatError,
    InvalidTypeError,
    InvalidValueError,
    format_duration,
    parse_duration,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("30s", 30),
        ("5m", 300),
        ("2h", 7200),
        ("1h30m", 5400),
        ("1h 30m 45s", 5445),
        ("1d2h", 93600),
        ("1w", 604800),
        ("1mo", 2592000),
        ("1y", 31536000),
        ("PT30S", 30),
        ("PT5M", 300),
        ("PT2H", 7200),
        ("PT1H30M45S", 5445),
        ("P1DT2H", 93600),
        ("P1M", 2592000),
        ("P1Y", 31536000),
        ("-30s", -30),
        ("-1h30m", -5400),
        ("+1h", 3600),
        (30, 30),
        (30.5, 30),
        (0, 0),
        (-60, -60),
    ],
)
def test_parse_duration_supported_inputs(
    value: str | int | float, expected: int
) -> None:
    assert parse_duration(value) == expected
    assert DurationAdapter.validate_python(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  30s  ", 30),
        ("\t1h30m\n", 5400),
        ("1 h 30 m", 5400),
        ("30 seconds", 30),
        ("2.5m", 150),
        ("30.9s", 30),
    ],
)
def test_parse_duration_whitespace_and_decimals(value: str, expected: int) -> None:
    assert parse_duration(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        "1x",
        "1 h junk",
        "P",
        "PT",
        "30",
    ],
)
def test_parse_duration_invalid_strings(value: str) -> None:
    with pytest.raises(InvalidFormatError):
        parse_duration(value)


@pytest.mark.parametrize(
    "value",
    ["", None, float("nan"), float("inf"), -float("inf")],
)
def test_parse_duration_invalid_values(value: object) -> None:
    with pytest.raises(InvalidValueError):
        parse_duration(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, False, object()])
def test_parse_duration_invalid_types(value: object) -> None:
    with pytest.raises(InvalidTypeError):
        parse_duration(value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "0s"),
        (30, "30s"),
        (90, "1m30s"),
        (3600, "1h"),
        (5400, "1h30m"),
        (-3600, "-1h"),
    ],
)
def test_format_duration(seconds: int, expected: str) -> None:
    assert format_duration(seconds) == expected


@pytest.mark.parametrize("value", [True, 30.5, "30s", None])
def test_format_duration_invalid_types(value: object) -> None:
    with pytest.raises(InvalidTypeError):
        format_duration(value)  # type: ignore[arg-type]


def test_error_hierarchy() -> None:
    assert issubclass(InvalidFormatError, DurationError)
    assert issubclass(InvalidTypeError, DurationError)
    assert issubclass(InvalidValueError, DurationError)


@given(st.integers(min_value=-10_000_000, max_value=10_000_000))
def test_format_parse_round_trip(seconds: int) -> None:
    assert parse_duration(format_duration(seconds)) == seconds


@given(
    st.floats(
        min_value=-10_000_000,
        max_value=10_000_000,
        allow_nan=False,
        allow_infinity=False,
    )
)
def test_float_inputs_truncate_toward_zero(value: float) -> None:
    assert parse_duration(value) == math.trunc(value)
