# Installation

Install from PyPI:

```bash
pip install duratypes
```

`duratypes` requires Python 3.12 or newer and Pydantic 2.5 or newer.

For development:

```bash
git clone https://github.com/dillon-barendt/duratypes.git
cd duratypes
uv sync --group dev
```

Run the local validation gate:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```
