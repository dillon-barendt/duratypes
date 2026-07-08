# Release

Releases use GitHub Actions and PyPI Trusted Publishing. Do not use long-lived
PyPI API tokens.

## Local Validation

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run python -m build
uv run twine check dist/*
```

## Wheel Smoke Test

```bash
python -m venv .venv-wheel-test
. .venv-wheel-test/bin/activate
python -m pip install --upgrade pip
python -m pip install dist/*.whl
python -c "from duratypes import parse_duration; assert parse_duration('1h30m') == 5400"
deactivate
rm -rf .venv-wheel-test
```

## Publishing

The release workflow publishes to TestPyPI from `main` or manual dispatch and
to PyPI from version tags such as `v0.1.0`.

Trusted Publishing environments:

- `testpypi`
- `pypi`

Release tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```
