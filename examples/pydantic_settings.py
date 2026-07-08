from pydantic import BaseModel, Field

from duratypes import Duration, DurationRange, PositiveDuration


class ServiceSettings(BaseModel):
    request_timeout: PositiveDuration = "30s"
    cache_ttl: Duration = "15m"
    retry_window: Duration = "1h"
    poll_interval: DurationRange = Field(
        default_factory=lambda: DurationRange(min="5s", max="1m")
    )


if __name__ == "__main__":
    settings = ServiceSettings()
    print(settings.model_dump())
