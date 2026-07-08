from duratypes.integrations.taskiq import retry_delay, schedule_every, task_timeout

TIMEOUT = task_timeout("2m")
RETRY_DELAY = retry_delay("30s")
SCHEDULE = schedule_every("5m")


if __name__ == "__main__":
    print(
        {
            "timeout": TIMEOUT,
            "retry_delay": RETRY_DELAY,
            "schedule": SCHEDULE,
        }
    )
