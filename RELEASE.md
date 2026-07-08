# Release Process

Use PyPI Trusted Publishing. Do not create or commit `.pypirc`, `twine.cfg`,
or long-lived PyPI API tokens.

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

## Clean Wheel Smoke Test

```bash
python -m venv .venv-wheel-test
. .venv-wheel-test/bin/activate
python -m pip install --upgrade pip
python -m pip install dist/*.whl
python -c "from duratypes import parse_duration; assert parse_duration('1h30m') == 5400"
deactivate
rm -rf .venv-wheel-test
```

## TestPyPI Install Test

```bash
python -m venv .venv-testpypi
. .venv-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ duratypes
python -c "from duratypes import parse_duration; assert parse_duration('1h30m') == 5400"
deactivate
rm -rf .venv-testpypi
```

## Trusted Publishing Setup

Configure PyPI:

```text
owner: dillon-barendt
repository: duratypes
workflow: release.yml
environment: pypi
```

Configure TestPyPI:

```text
owner: dillon-barendt
repository: duratypes
workflow: release.yml
environment: testpypi
```

## Publish Flow

1. Run local validation.
2. Push to `main` to publish to TestPyPI after CI-quality checks pass.
3. Run the TestPyPI install smoke test.
4. Tag the release only after TestPyPI validation succeeds.

```bash
git tag v0.1.0
git push origin v0.1.0
```

The `release.yml` workflow publishes version tags to PyPI with Trusted
Publishing.
