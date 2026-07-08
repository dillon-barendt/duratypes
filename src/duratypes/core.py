import logging
import math
import re
from datetime import timedelta
from typing import Annotated, Self

from pydantic import BaseModel, BeforeValidator, Field, TypeAdapter, model_validator


# Custom exception hierarchy
class DurationError(ValueError):
    """Base exception for all duration-related errors."""

    pass


class InvalidFormatError(DurationError):
    """Raised when a duration string has an invalid format."""

    pass


class InvalidTypeError(DurationError, TypeError):
    """Raised when an invalid type is provided for duration parsing."""

    pass


class InvalidValueError(DurationError):
    """Raised when a duration value is invalid (e.g., None, NaN)."""

    pass


# Constants for time unit conversions
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = 604800  # 7 * 24 * 60 * 60
SECONDS_PER_MONTH = 2592000  # 30 * 24 * 60 * 60 (approximate)
SECONDS_PER_YEAR = 31536000  # 365 * 24 * 60 * 60 (approximate)
MILLISECONDS_PER_SECOND = 1000

type DurationInput = str | int | float

_UNIT_MULTIPLIERS = {
    "y": SECONDS_PER_YEAR,
    "mo": SECONDS_PER_MONTH,
    "w": SECONDS_PER_WEEK,
    "d": SECONDS_PER_DAY,
    "h": SECONDS_PER_HOUR,
    "m": SECONDS_PER_MINUTE,
    "s": 1,
}

# Logger for debugging
logger = logging.getLogger(__name__)

__all__ = [
    "Duration",
    "DurationAdapter",
    "DurationError",
    "DurationInput",
    "DurationRange",
    "Hours",
    "InvalidFormatError",
    "InvalidTypeError",
    "InvalidValueError",
    "Milliseconds",
    "Minutes",
    "NonNegativeDuration",
    "PositiveDuration",
    "Seconds",
    "format_duration",
    "parse_duration",
    "to_iso8601",
    "to_milliseconds",
    "to_seconds",
    "to_timedelta",
]

_COMPOUND_RE = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>y(?:ear)?s?|mo(?:nth)?s?|w(?:eek)?s?|d(?:ay)?s?|h(?:our)?s?|m(?:in(?:ute)?s?)?|s(?:ec(?:ond)?s?)?)",
    re.IGNORECASE,
)
_ISO_RE = re.compile(
    r"^(?P<sign>[+-])?P"
    r"(?:(?P<y>[+-]?\d+(?:\.\d+)?)Y)?"
    r"(?:(?P<mo>[+-]?\d+(?:\.\d+)?)M)?"
    r"(?:(?P<d>[+-]?\d+(?:\.\d+)?)D)?"
    r"(?:T"
    r"(?:(?P<h>[+-]?\d+(?:\.\d+)?)H)?"
    r"(?:(?P<m>[+-]?\d+(?:\.\d+)?)M)?"
    r"(?:(?P<s>[+-]?\d+(?:\.\d+)?)S)?)?$",
    re.IGNORECASE,
)
_LEADING_SIGN = re.compile(r"^(?P<sign>[+-])\s*(?P<rest>.*)$")


def _validate_input(v: object) -> None:
    """Validate input type and basic constraints."""
    if v is None:
        raise InvalidValueError("Duration cannot be None")
    if isinstance(v, bool):
        raise InvalidTypeError("Duration cannot be a boolean")


def _parse_numeric_seconds(v: int | float) -> float:
    """Parse numeric duration input."""
    if not isinstance(v, int | float) or not math.isfinite(v):
        raise InvalidValueError(f"Invalid numeric duration: {v!r}")
    logger.debug(f"Parsing numeric duration: {v}")
    return float(v)


def _extract_sign(raw: str, original: DurationInput) -> tuple[str, int]:
    """Extract leading sign from duration string."""
    sign = 1
    m_sign = _LEADING_SIGN.match(raw)
    if m_sign:
        raw = m_sign.group("rest").strip()
        sign = -1 if m_sign.group("sign") == "-" else 1
        if not raw:
            raise InvalidFormatError(
                f"Invalid duration format: missing duration after sign in {original!r}"
            )
    return raw, sign


def _parse_iso8601_seconds(raw: str, sign: int) -> float | None:
    """Parse ISO 8601 duration format."""
    m_iso = _ISO_RE.fullmatch(raw)
    if not m_iso:
        return None

    logger.debug(f"Matched ISO 8601 format: {raw}")
    if m_iso.group("sign"):
        sign = -1 if m_iso.group("sign") == "-" else +1

    if not any(
        m_iso.group(name) is not None for name in ("y", "mo", "d", "h", "m", "s")
    ):
        return None

    # Parse individual components. Years and months are fixed approximations.
    y = float(m_iso.group("y") or 0)
    mo = float(m_iso.group("mo") or 0)
    d = float(m_iso.group("d") or 0)
    h = float(m_iso.group("h") or 0)
    minutes = float(m_iso.group("m") or 0)
    s = float(m_iso.group("s") or 0)

    total_seconds = (
        y * SECONDS_PER_YEAR
        + mo * SECONDS_PER_MONTH
        + d * SECONDS_PER_DAY
        + h * SECONDS_PER_HOUR
        + minutes * SECONDS_PER_MINUTE
        + s
    )
    return sign * total_seconds


def _parse_compound_seconds(raw: str, sign: int) -> float | None:
    """Parse compound duration format (e.g., '1h30m45s')."""
    total = 0.0
    matches = list(_COMPOUND_RE.finditer(raw.lower()))

    if not matches:
        return None

    # Check that matches cover the entire string without gaps
    expected_pos = 0
    for match in matches:
        # Skip whitespace before the match
        while expected_pos < len(raw) and raw[expected_pos].isspace():
            expected_pos += 1

        # Check if match starts where we expect
        if match.start() != expected_pos:
            # There's a gap or unexpected characters
            return None

        val = float(match.group("value"))
        unit = match.group("unit").lower().strip()
        key = "mo" if unit.startswith("mo") else unit[0]
        multiplier = _UNIT_MULTIPLIERS[key]
        total += val * multiplier

        expected_pos = match.end()

        logger.debug(f"Parsed component: {val}{unit} -> {val * multiplier} seconds")

    # Check that we've consumed the entire string (ignoring trailing whitespace)
    while expected_pos < len(raw) and raw[expected_pos].isspace():
        expected_pos += 1

    if expected_pos != len(raw):
        # There are unconsumed characters
        return None

    return sign * total


def _parse_duration_seconds(v: DurationInput) -> float:
    """Parse duration input into seconds, preserving fractional precision."""
    _validate_input(v)

    if isinstance(v, int | float):
        return _parse_numeric_seconds(v)

    if not isinstance(v, str):
        raise InvalidTypeError(
            f"Duration must be str, int, or float, got {type(v).__name__}"
        )

    raw = str(v).strip()
    if not raw:
        raise InvalidValueError("Duration string cannot be empty")

    logger.debug(f"Parsing duration string: {raw!r}")

    raw, sign = _extract_sign(raw, v)

    result = _parse_iso8601_seconds(raw, sign)
    if result is not None:
        return result

    result = _parse_compound_seconds(raw, sign)
    if result is not None:
        return result

    raise InvalidFormatError(
        f"Invalid duration format: {v!r}. "
        f"Supported formats: compound ('30s', '5m', '1h30m'), "
        f"ISO 8601 ('PT30S', 'PT5M', 'PT1H30M'), or numeric (30, 30.5)"
    )


def parse_duration(v: DurationInput) -> int:
    """
    Parse a duration string, integer, or float into seconds.

    Args:
        v: Duration input in various formats:
            - String: "30s", "5m", "1h30m", "PT1H30M", etc.
            - Integer/Float: Direct seconds value

    Returns:
        Duration in seconds as an integer

    Raises:
        InvalidFormatError: If the input format is invalid or unsupported
        InvalidTypeError: If the input type is not supported
        InvalidValueError: If the input value is invalid (None, NaN, empty string)
    """
    return int(_parse_duration_seconds(v))


def to_seconds(value: DurationInput) -> int:
    """Convert duration input to normalized integer seconds."""
    return parse_duration(value)


def to_milliseconds(value: DurationInput) -> int:
    """Convert duration input to normalized integer milliseconds.

    Fractional seconds are preserved to millisecond precision and then truncated
    toward zero. Numeric input is interpreted as seconds.
    """
    return int(_parse_duration_seconds(value) * MILLISECONDS_PER_SECOND)


def to_timedelta(value: DurationInput) -> timedelta:
    """Convert duration input to ``datetime.timedelta``.

    Fractional seconds are preserved for string and numeric inputs.
    """
    return timedelta(seconds=_parse_duration_seconds(value))


def to_iso8601(value: DurationInput) -> str:
    """Convert duration input to a compact ISO 8601 duration string.

    The output uses normalized integer seconds and does not emit calendar month
    or year components.
    """
    seconds = to_seconds(value)
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)

    days, rem = divmod(seconds, SECONDS_PER_DAY)
    hours, rem = divmod(rem, SECONDS_PER_HOUR)
    minutes, secs = divmod(rem, SECONDS_PER_MINUTE)

    if seconds == 0:
        return "PT0S"

    date_part = f"{days}D" if days else ""
    time_parts = []
    if hours:
        time_parts.append(f"{hours}H")
    if minutes:
        time_parts.append(f"{minutes}M")
    if secs:
        time_parts.append(f"{secs}S")

    if time_parts:
        return f"{sign}P{date_part}T{''.join(time_parts)}"
    return f"{sign}P{date_part}"


def format_duration(seconds: int) -> str:
    """
    Format a duration in seconds into a human-readable string.

    Args:
        seconds: Duration in seconds (can be negative)

    Returns:
        Human-readable duration string (e.g., "1h30m45s", "30s", "-2h15m")

    Raises:
        InvalidTypeError: If seconds is not an integer
    """
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise InvalidTypeError(
            f"Seconds must be an integer, got {type(seconds).__name__}"
        )

    logger.debug(f"Formatting duration: {seconds} seconds")

    sign_str = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    parts = []

    # Break down into largest units first
    y, rem = divmod(seconds, SECONDS_PER_YEAR)
    mo, rem = divmod(rem, SECONDS_PER_MONTH)
    w, rem = divmod(rem, SECONDS_PER_WEEK)
    d, rem = divmod(rem, SECONDS_PER_DAY)
    h, rem = divmod(rem, SECONDS_PER_HOUR)
    m, s = divmod(rem, SECONDS_PER_MINUTE)

    if y:
        parts.append(f"{y}y")
    if mo:
        parts.append(f"{mo}mo")
    if w:
        parts.append(f"{w}w")
    if d:
        parts.append(f"{d}d")
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s or not parts:  # Always include seconds if it's the only component
        parts.append(f"{s}s")

    result = sign_str + "".join(parts)
    logger.debug(f"Formatted duration result: {result}")
    return result


# Pydantic annotated types. Defaults are validated so `Duration = "30s"` works.
_DurationCore = Annotated[int, BeforeValidator(parse_duration)]
Duration = Annotated[
    int,
    BeforeValidator(parse_duration),
    Field(validate_default=True),
]
NonNegativeDuration = Annotated[
    int,
    BeforeValidator(parse_duration),
    Field(ge=0, validate_default=True),
]
PositiveDuration = Annotated[
    int,
    BeforeValidator(parse_duration),
    Field(gt=0, validate_default=True),
]
Milliseconds = Annotated[
    int,
    BeforeValidator(to_milliseconds),
    Field(validate_default=True),
]
Seconds = Duration
Minutes = Duration
Hours = Duration

# Singleton adapter for maximum reuse
DurationAdapter: TypeAdapter[int] = TypeAdapter(_DurationCore)


class DurationRange(BaseModel):
    """Inclusive duration range with normalized integer-second bounds."""

    min: NonNegativeDuration
    max: PositiveDuration

    @model_validator(mode="after")
    def _validate_bounds(self) -> Self:
        if self.min > self.max:
            raise ValueError("DurationRange min must be less than or equal to max")
        return self
