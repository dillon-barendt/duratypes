from duratypes import DurationAdapter
from duratypes.integrations.fastapi import DurationQuery

try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None


def health(timeout: DurationQuery = "30s") -> dict[str, int]:
    return {"timeout_seconds": DurationAdapter.validate_python(timeout)}


if FastAPI is not None:
    app = FastAPI()
    app.get("/health")(health)


if __name__ == "__main__":
    print(health())
