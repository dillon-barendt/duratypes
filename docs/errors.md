# Errors

`duratypes` exposes a small exception hierarchy.

## `DurationError`

Base class for package-specific errors.

## `InvalidFormatError`

Raised when a string has unsupported syntax:

```python
parse_duration("1x")
parse_duration("1 h junk")
parse_duration("30")
```

## `InvalidTypeError`

Raised for unsupported types:

```python
parse_duration(True)
parse_duration(object())
format_duration(30.5)
```

## `InvalidValueError`

Raised for invalid values:

```python
parse_duration("")
parse_duration(None)
parse_duration(float("nan"))
parse_duration(float("inf"))
```

Inside Pydantic models these become normal `ValidationError` instances.
