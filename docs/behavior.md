# Behavior

## Supported Inputs

Compound strings:

```python
parse_duration("30s")          # 30
parse_duration("5m")           # 300
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
parse_duration("P1M")          # 2592000
parse_duration("P1Y")          # 31536000
```

Numeric values are seconds. Floats truncate toward zero.

Serialization helpers have explicit precision behavior:

- `to_seconds()` returns normalized integer seconds.
- `to_milliseconds()` preserves fractional seconds to millisecond precision and
  truncates toward zero.
- `to_timedelta()` preserves fractional seconds.
- `to_iso8601()` emits normalized integer seconds and does not emit calendar
  month or year components.

## Validation Rules

- Leading and trailing whitespace is ignored.
- Whitespace between compound units is allowed.
- A leading `+` or `-` is allowed.
- Empty strings are invalid.
- Strings without units, such as `"30"`, are invalid.
- `None`, booleans, `NaN`, and infinities are invalid.

## Month and Year Policy

Months and years are fixed approximations:

- `1mo` equals 30 days.
- `1y` equals 365 days.

This is useful for coarse config windows but is not calendar-aware. Use a
calendar library for billing cycles, recurring events, or date arithmetic.
