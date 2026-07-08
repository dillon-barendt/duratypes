# Pydantic

`Duration` works in Pydantic v2 models and validates defaults.

```python
from pydantic import BaseModel

from duratypes import Duration


class Settings(BaseModel):
    timeout: Duration
    retry_delay: Duration = "30s"


settings = Settings(timeout="1h30m")
assert settings.timeout == 5400
assert settings.retry_delay == 30
```

Field constraints run after parsing:

```python
from pydantic import BaseModel, Field

from duratypes import Duration


class RetryPolicy(BaseModel):
    timeout: Duration = Field(gt=0)


assert RetryPolicy(timeout="30s").timeout == 30
```

JSON schema describes the normalized runtime value as integer seconds:

```python
schema = RetryPolicy.model_json_schema()
assert schema["properties"]["timeout"]["type"] == "integer"
```

`PositiveDuration` and `NonNegativeDuration` add Pydantic constraints after
parsing:

```python
from pydantic import BaseModel

from duratypes import NonNegativeDuration, PositiveDuration


class TimeoutBudget(BaseModel):
    timeout: PositiveDuration = "30s"
    grace_period: NonNegativeDuration = "0s"
```

`DurationRange` validates inclusive min/max bounds:

```python
from duratypes import DurationRange

window = DurationRange(min="5s", max="1m")
assert window.min == 5
assert window.max == 60
```

`Seconds`, `Minutes`, and `Hours` are semantic aliases. They all store seconds.
`Milliseconds` is intentionally separate and stores integer milliseconds.
