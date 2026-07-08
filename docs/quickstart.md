# Quick Start

```python
from duratypes import format_duration, parse_duration

assert parse_duration("30s") == 30
assert parse_duration("5m") == 300
assert parse_duration("1h30m") == 5400
assert parse_duration("PT1H30M") == 5400

assert format_duration(5400) == "1h30m"
```

Numeric values are treated as seconds:

```python
assert parse_duration(30) == 30
assert parse_duration(30.5) == 30
assert parse_duration(-60) == -60
```

Use `DurationAdapter` when you want Pydantic validation without defining a
model:

```python
from duratypes import DurationAdapter

assert DurationAdapter.validate_python("15m") == 900
```
