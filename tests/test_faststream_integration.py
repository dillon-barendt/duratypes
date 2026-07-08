import pytest

from duratypes import InvalidValueError
from duratypes.integrations.faststream import message_ttl_headers, retry_headers


def test_message_ttl_headers_use_milliseconds() -> None:
    assert message_ttl_headers("15m")["x-message-ttl-ms"] == "900000"


def test_retry_headers_include_seconds_and_milliseconds() -> None:
    assert retry_headers("1.5s") == {
        "retry-after": "1",
        "x-retry-after-ms": "1500",
    }


def test_faststream_headers_reject_negative_values() -> None:
    with pytest.raises(InvalidValueError):
        message_ttl_headers("-1s")
