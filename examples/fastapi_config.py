from pydantic import BaseModel

from duratypes import Duration


class FastAPISettings(BaseModel):
    request_timeout: Duration = "30s"
    cache_ttl: Duration = "10m"
    background_task_timeout: Duration = "2m"


settings = FastAPISettings()


def get_settings() -> FastAPISettings:
    return settings


if __name__ == "__main__":
    print(get_settings().model_dump())
