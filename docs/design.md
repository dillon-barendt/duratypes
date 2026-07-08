# Design

`Duration` is a value primitive, not a framework object.

The core package parses ergonomic duration input and normalizes it into typed
runtime values. Framework integrations should consume those values, not own
them.

## Core stays small

The base install depends on Pydantic and keeps duration parsing, formatting,
serialization, and validation in one focused package.

```bash
pip install duratypes
```

## Integrations stay optional

Integration modules live under `duratypes.integrations`. They provide helpers
for service configuration, async task queues, message streams, agent runtimes,
and graph workflows.

Optional extras carry framework-specific dependencies only when the helper
actually imports that framework. Dependency-free helpers remain available from
the base package.

## Duration values stay simple

Most public types normalize to integer seconds:

- `Duration`
- `PositiveDuration`
- `NonNegativeDuration`
- `Seconds`
- `Minutes`
- `Hours`

`Milliseconds` is intentionally separate and normalizes to integer
milliseconds. Numeric input is still interpreted as seconds before conversion to
milliseconds.
