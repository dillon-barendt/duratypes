from dataclasses import dataclass

from duratypes import parse_duration


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    initial_delay: int
    max_window: int


def build_retry_policy() -> RetryPolicy:
    return RetryPolicy(
        max_attempts=3,
        initial_delay=parse_duration("1s"),
        max_window=parse_duration("2m"),
    )


if __name__ == "__main__":
    print(build_retry_policy())
