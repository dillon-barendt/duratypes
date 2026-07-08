# API

## Functions

`parse_duration(value: str | int | float) -> int`

Parses supported duration input into integer seconds.

`format_duration(seconds: int) -> str`

Formats integer seconds as a compact duration string such as `1h30m`.

`to_seconds(value: str | int | float) -> int`

Converts supported duration input to integer seconds.

`to_milliseconds(value: str | int | float) -> int`

Converts supported duration input to integer milliseconds. Fractional seconds
are preserved to millisecond precision before truncation.

`to_timedelta(value: str | int | float) -> datetime.timedelta`

Converts supported duration input to `datetime.timedelta`.

`to_iso8601(value: str | int | float) -> str`

Converts supported duration input to a compact ISO 8601 string using normalized
integer seconds.

## Pydantic Types

`Duration`, `PositiveDuration`, `NonNegativeDuration`, `Seconds`, `Minutes`, and
`Hours` are semantic aliases for a Pydantic-validated integer. All values
normalize to integer seconds.

`Milliseconds` is separate and normalizes to integer milliseconds. Numeric input
is interpreted as seconds before conversion.

```python
from pydantic import BaseModel

from duratypes import Duration, PositiveDuration


class Settings(BaseModel):
    timeout: Duration
    retry_delay: PositiveDuration = "5s"


assert Settings(timeout="1h").timeout == 3600
```

## DurationRange

`DurationRange` models inclusive duration bounds:

```python
from duratypes import DurationRange

window = DurationRange(min="5s", max="1m")
assert window.min == 5
assert window.max == 60
```

## Adapter

`DurationAdapter` is a reusable Pydantic `TypeAdapter`:

```python
from duratypes import DurationAdapter

assert DurationAdapter.validate_python("1h30m") == 5400
```

## Exceptions

- `DurationError`
- `InvalidFormatError`
- `InvalidTypeError`
- `InvalidValueError`
