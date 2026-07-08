# duratypes

[![CI](https://github.com/dillon-barendt/duratypes/actions/workflows/ci.yml/badge.svg)](https://github.com/dillon-barendt/duratypes/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Fast, typed duration parsing for Pydantic and modern Python apps.

`duratypes` turns human-readable duration values like `30s`, `5m`,
`1h30m`, and `PT1H30M` into typed integer seconds that work cleanly
inside Pydantic v2 models.

## Why duratypes?

Python services often accept duration values from environment variables, YAML
files, CLI flags, API payloads, and user-facing configuration. Those values are
usually strings at the boundary but need to become precise values inside the
program.

`duratypes` is a small primitive for that boundary:

- parse ergonomic duration strings into integer seconds
- use the same behavior directly or inside Pydantic v2 models
- keep timeout, retry, TTL, scheduling, and async configuration readable
- fail with specific errors when input is invalid

## Design Philosophy

Python applications often accept duration values from environment variables,
YAML files, CLI flags, API payloads, and user-facing config. Those values are
usually strings at the boundary but need to become precise, typed values inside
the program.

`duratypes` focuses on that boundary: accepting ergonomic duration input and
normalizing it into simple integer seconds that are easy to store, compare,
validate, and pass to async/runtime APIs.

## Beyond parsing: typed duration primitives for modern Python infrastructure

`duratypes` starts with a tiny core: parse human-readable duration values and
normalize them into typed values for Pydantic models.

The roadmap extends that primitive into optional helpers for service
configuration, async task queues, message streams, agent runtimes, and graph
workflows.

The base package stays small. Framework integrations are optional.

- [Integration docs](docs/integrations.md)
- [Roadmap](docs/roadmap.md)
- [Design notes](docs/design.md)

## Install

```bash
pip install duratypes
```

## Quick Start

```python
from duratypes import format_duration, parse_duration

assert parse_duration("30s") == 30
assert parse_duration("5m") == 300
assert parse_duration("1h30m") == 5400
assert parse_duration("PT1H30M") == 5400
assert format_duration(5400) == "1h30m"
```

Async timeout config stays readable at the boundary:

```python
from duratypes import parse_duration

timeout_seconds = parse_duration("2.5m")
```

## Pydantic Settings Example

```python
from pydantic import BaseModel

from duratypes import Duration


class ServiceSettings(BaseModel):
    request_timeout: Duration = "30s"
    cache_ttl: Duration = "15m"
    retry_window: Duration = "1h"


settings = ServiceSettings()
assert settings.request_timeout == 30
assert settings.cache_ttl == 900
assert settings.retry_window == 3600
```

Validation errors are normal Pydantic errors:

```python
from pydantic import BaseModel, ValidationError

from duratypes import Duration


class Settings(BaseModel):
    timeout: Duration


try:
    Settings(timeout="forever")
except ValidationError as exc:
    print(exc)
```

## Supported Inputs

Compound strings:

```python
parse_duration("30s")          # 30
parse_duration("5m")           # 300
parse_duration("2h")           # 7200
parse_duration("1h30m")        # 5400
parse_duration("1h 30m 45s")   # 5445
parse_duration("1d2h")         # 93600
parse_duration("1w")           # 604800
parse_duration("1mo")          # 2592000
parse_duration("1y")           # 31536000
```

ISO 8601 duration strings:

```python
parse_duration("PT30S")        # 30
parse_duration("PT5M")         # 300
parse_duration("PT2H")         # 7200
parse_duration("PT1H30M45S")   # 5445
parse_duration("P1DT2H")       # 93600
```

Numeric seconds:

```python
parse_duration(30)             # 30
parse_duration(30.5)           # 30
parse_duration(0)              # 0
parse_duration(-60)            # -60
```

## Public API

```python
parse_duration
format_duration
Duration
PositiveDuration
NonNegativeDuration
Milliseconds
Seconds
Minutes
Hours
DurationRange
DurationAdapter
DurationError
InvalidFormatError
InvalidTypeError
InvalidValueError
to_seconds
to_milliseconds
to_timedelta
to_iso8601
```

`Duration`, `PositiveDuration`, `NonNegativeDuration`, `Seconds`, `Minutes`,
and `Hours` are semantic aliases. They all normalize to integer seconds;
`Minutes` does not store minutes and `Hours` does not store hours.

`Milliseconds` is intentionally separate and normalizes to integer milliseconds.
Numeric input is interpreted as seconds before conversion to milliseconds.

`DurationAdapter` is a reusable Pydantic `TypeAdapter` for validation outside a
model:

```python
from duratypes import DurationAdapter

assert DurationAdapter.validate_python("1h30m") == 5400
```

`DurationRange` models inclusive min/max bounds:

```python
from duratypes import DurationRange

window = DurationRange(min="5s", max="1m")
assert window.min == 5
assert window.max == 60
```

Serialization helpers convert duration input into common runtime forms:

```python
from datetime import timedelta

from duratypes import to_iso8601, to_milliseconds, to_seconds, to_timedelta

assert to_seconds("1h30m") == 5400
assert to_milliseconds("1.5s") == 1500
assert to_timedelta("5m") == timedelta(minutes=5)
assert to_iso8601("1h30m") == "PT1H30M"
```

## Optional Integrations

Integration helpers live under `duratypes.integrations` and keep framework
coupling outside the core package.

```python
from duratypes.integrations.faststream import message_ttl_headers
from duratypes.integrations.taskiq import retry_delay, task_timeout

assert task_timeout("2m") == 120
assert retry_delay("30s") == 30
assert message_ttl_headers("15m")["x-message-ttl-ms"] == "900000"
```

FastAPI parameter helper functions require the optional extra:

```bash
pip install "duratypes[fastapi]"
```

## Behavior Notes

- Strings are stripped before parsing, and whitespace between components is
  allowed.
- Numeric input is treated as seconds.
- Float input truncates toward zero using `int(...)`.
- Negative durations are supported with a leading `-`.
- Leading `+` is accepted.
- Empty strings, unsupported units, `None`, booleans, `NaN`, and infinities are
  rejected.
- Months and years are fixed approximations: `1mo` is 30 days, and `1y` is 365
  days. These are not calendar-aware durations.
- `format_duration()` returns compact compound strings such as `1h30m`.

## Error Handling

`duratypes` raises a small exception hierarchy:

- `DurationError`: base class
- `InvalidFormatError`: malformed duration strings
- `InvalidTypeError`: unsupported input types such as `bool` or `object`
- `InvalidValueError`: invalid values such as `None`, empty strings, `NaN`, or
  infinity

```python
from duratypes import InvalidFormatError, parse_duration

try:
    parse_duration("1x")
except InvalidFormatError:
    print("not a supported duration")
```

## Performance Notes

The parser uses compiled regular expressions, stores durations as integer
seconds, and exposes a singleton `DurationAdapter` for repeated Pydantic
validation. The normal test suite avoids fragile benchmarks; use the benchmark
script for local smoke checks:

```bash
python benchmarks/parse_duration.py
```

## When to Use This

Use `duratypes` when your application accepts human-readable durations for:

- request timeouts
- cache TTLs
- retry windows
- scheduling intervals
- Pydantic/FastAPI configuration models
- async runtime settings that expect seconds

## When Not to Use This

Do not use `duratypes` when you need calendar-aware arithmetic. Months and years
are fixed approximations, so use `datetime`, `dateutil`, or a domain-specific
calendar library for billing cycles, recurring events, or date math.

## Development

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run python -m build
uv run twine check dist/*
```

## Release Process

Releases are built by GitHub Actions and published with PyPI Trusted Publishing.
No long-lived PyPI API tokens are required.

Local validation:

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run python -m build
uv run twine check dist/*
```

Publish to PyPI only from a version tag after CI passes:

```bash
git tag v0.1.0
git push origin v0.1.0
```

See [RELEASE.md](RELEASE.md) for the full release checklist.

## License

MIT. See [LICENSE](LICENSE).
