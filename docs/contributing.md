# Contributing

Keep contributions small and aligned with the package goal: typed duration
parsing for Pydantic and modern Python apps.

## Development Setup

```bash
uv sync --group dev
```

## Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

## Guidelines

- Preserve the public API unless a breaking change is intentional.
- Add tests for parser behavior and Pydantic integration.
- Keep runtime dependencies minimal.
- Document behavior changes in `CHANGELOG.md`.
