from __future__ import annotations

from time import perf_counter

from pydantic import BaseModel

from duratypes import Duration, DurationAdapter, parse_duration


class Settings(BaseModel):
    timeout: Duration


VALUES = ["30s", "5m", "1h30m", "PT1H30M", "1d2h"]
ITERATIONS = 50_000


def time_loop(label: str, fn) -> None:
    started = perf_counter()
    for _ in range(ITERATIONS):
        for value in VALUES:
            fn(value)
    elapsed = perf_counter() - started
    total = ITERATIONS * len(VALUES)
    print(f"{label}: {elapsed:.4f}s total, {(elapsed / total) * 1_000_000:.2f} us/op")


def main() -> None:
    time_loop("parse_duration", parse_duration)
    time_loop("DurationAdapter.validate_python", DurationAdapter.validate_python)
    time_loop("Pydantic model", lambda value: Settings(timeout=value))


if __name__ == "__main__":
    main()
