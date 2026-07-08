# duratypes

Fast, typed duration parsing for Pydantic and modern Python apps.

`duratypes` converts boundary values such as `30s`, `5m`, `1h30m`, and
`PT1H30M` into integer seconds. That makes configuration values readable while
keeping runtime code simple.

```python
from duratypes import parse_duration

assert parse_duration("1h30m") == 5400
```

Use it for service timeouts, cache TTLs, retry windows, scheduling intervals,
and settings models where input should be ergonomic but internal values should
be exact integer seconds.

## Core Ideas

- Parse human-readable strings at the boundary.
- Store and compare normalized integer seconds.
- Integrate directly with Pydantic v2.
- Keep the package small and dependency-light.

## Next Steps

- [Install](installation.md)
- [Quick Start](quickstart.md)
- [Pydantic Integration](pydantic.md)
- [Behavior Notes](behavior.md)
- [Integrations](integrations.md)
- [Design](design.md)
- [Roadmap](roadmap.md)
