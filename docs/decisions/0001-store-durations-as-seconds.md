# 0001: Store Durations as Integer Seconds

## Status

Accepted.

## Context

Application configuration often needs human-readable durations at the boundary
and simple values inside the program. Timeouts, TTLs, retry windows, and
scheduling intervals are commonly passed to runtime APIs as seconds.

## Decision

`duratypes` normalizes supported duration input to integer seconds.

## Consequences

Integer seconds are easy to compare, serialize, validate, and pass to async or
runtime APIs. Pydantic models can expose readable defaults while application
code receives simple integers.

The tradeoff is that calendar-aware durations are out of scope. Months and
years are fixed approximations: one month is 30 days, and one year is 365 days.
This is appropriate for coarse configuration windows but not for billing cycles,
recurring calendar events, or date arithmetic.
