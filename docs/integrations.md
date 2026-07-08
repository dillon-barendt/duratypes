# Integrations

## Core principle

`duratypes` keeps duration parsing in the core package and exposes optional
helpers for frameworks that commonly need timeout, retry, TTL, and scheduling
values.

The core type remains a value primitive. Framework integrations consume
durations; they do not own the duration model.

## FastAPI

`duratypes.integrations.fastapi` exposes `DurationQuery`, `DurationHeader`, and
`DurationPath` aliases plus helper functions for FastAPI parameter defaults.

```python
from duratypes import Duration
from duratypes.integrations.fastapi import duration_query


def health(timeout: Duration = duration_query("30s")):
    return {"timeout_seconds": timeout}
```

Install the optional extra when using the helper functions:

```bash
pip install "duratypes[fastapi]"
```

The aliases are dependency-free. The helper functions import FastAPI only when
called.

## Taskiq

`duratypes.integrations.taskiq` provides dependency-free primitives for task
timeouts, retry delays, and schedule metadata.

```python
from duratypes.integrations.taskiq import retry_delay, task_timeout

TIMEOUT = task_timeout("2m")
RETRY_DELAY = retry_delay("30s")
```

These helpers return plain integers or dictionaries and do not require a broker.

## FastStream

`duratypes.integrations.faststream` provides broker-neutral header helpers.

```python
from duratypes.integrations.faststream import message_ttl_headers

headers = message_ttl_headers("15m")
assert headers["x-message-ttl-ms"] == "900000"
```

No Kafka, RabbitMQ, Redis, or NATS dependency is required.

## Pydantic AI

`duratypes.integrations.pydantic_ai` provides plain Pydantic models for agent
runtime budgets.

```python
from duratypes.integrations.pydantic_ai import RunBudget

budget = RunBudget(max_duration="2m", retry_delay="5s")
```

This module does not require Pydantic AI because it intentionally models
duration budgets without coupling to agent runtime internals.

## Pydantic Graph

`duratypes.integrations.pydantic_graph` provides timeout guard primitives for
graph-style workflows.

```python
from datetime import UTC, datetime

from duratypes.integrations.pydantic_graph import TimeoutGuard

guard = TimeoutGuard(max_duration="10m")
assert guard.expired(datetime.now(UTC), now=datetime.now(UTC)) is False
```

## Dependency policy

The base install stays lightweight:

```bash
pip install duratypes
```

Framework dependencies are added only when an integration directly imports that
framework. In this phase, the only framework extra is:

```bash
pip install "duratypes[fastapi]"
```

Taskiq, FastStream, Pydantic AI, and Pydantic Graph helpers are dependency-free
plain Python/Pydantic primitives for now.
