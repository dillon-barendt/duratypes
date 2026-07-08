from importlib.util import find_spec

import pytest
from pydantic import TypeAdapter

from duratypes.integrations.fastapi import (
    DurationHeader,
    DurationPath,
    DurationQuery,
    duration_query,
)


def test_fastapi_aliases_validate_without_fastapi_installed() -> None:
    assert TypeAdapter(DurationQuery).validate_python("30s") == 30
    assert TypeAdapter(DurationHeader).validate_python("1m") == 60
    assert TypeAdapter(DurationPath).validate_python("2m") == 120


def test_duration_query_helper_is_import_safe() -> None:
    if find_spec("fastapi") is None:
        with pytest.raises(ImportError, match="duratypes\\[fastapi\\]"):
            duration_query("30s")
    else:
        assert duration_query("30s") is not None
