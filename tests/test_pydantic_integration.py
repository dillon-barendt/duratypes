import pytest
from pydantic import BaseModel, Field, ValidationError

from duratypes import Duration, Hours, Minutes, Seconds


def test_duration_fields_parse_model_input_and_defaults() -> None:
    class Settings(BaseModel):
        timeout: Duration
        retry_delay: Duration = "30s"

    settings = Settings(timeout="1h30m")

    assert settings.timeout == 5400
    assert settings.retry_delay == 30


def test_semantic_aliases_store_integer_seconds() -> None:
    class Schedule(BaseModel):
        seconds: Seconds
        minutes: Minutes
        hours: Hours

    schedule = Schedule(seconds="1h", minutes="1h", hours="1h")

    assert schedule.seconds == 3600
    assert schedule.minutes == 3600
    assert schedule.hours == 3600


def test_field_constraints_run_after_duration_parsing() -> None:
    class RetryPolicy(BaseModel):
        timeout: Duration = Field(gt=0)

    assert RetryPolicy(timeout="30s").timeout == 30

    with pytest.raises(ValidationError):
        RetryPolicy(timeout="-30s")


def test_invalid_duration_becomes_pydantic_validation_error() -> None:
    class Settings(BaseModel):
        timeout: Duration

    with pytest.raises(ValidationError) as exc_info:
        Settings(timeout="not-a-duration")

    assert "timeout" in str(exc_info.value)
    assert "Invalid duration format" in str(exc_info.value)


def test_json_schema_describes_normalized_integer_seconds() -> None:
    class Settings(BaseModel):
        timeout: Duration = Field(description="Request timeout in seconds")

    schema = Settings.model_json_schema()
    timeout = schema["properties"]["timeout"]

    assert timeout["type"] == "integer"
    assert timeout["description"] == "Request timeout in seconds"
    assert schema["required"] == ["timeout"]


def test_model_dump_uses_normalized_seconds() -> None:
    class Settings(BaseModel):
        request_timeout: Duration = "30s"
        cache_ttl: Duration = "15m"

    settings = Settings()

    assert settings.model_dump() == {
        "request_timeout": 30,
        "cache_ttl": 900,
    }
