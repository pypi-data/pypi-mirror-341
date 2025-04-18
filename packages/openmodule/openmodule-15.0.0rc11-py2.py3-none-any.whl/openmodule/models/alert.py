from enum import StrEnum

from pydantic import field_validator
from typing import Dict, Optional

from openmodule.models.base import ZMQMessage


class AlertStatus(StrEnum):
    ok = "ok"
    error = "error"
    offline = "offline"


class AlertHandleType(StrEnum):
    state = "state"
    state_change = "state_change"
    count = "count"


class AlertMessage(ZMQMessage):
    type: str = "alert"
    status: AlertStatus
    alert_meta: Dict
    package: str
    alert_type: str
    source: Optional[str] = None
    handle_type: AlertHandleType
    value: Optional[float] = None

    @field_validator("value")
    def require_value_for_state_type(cls, v, values):
        if values.data["handle_type"] == AlertHandleType.state:
            assert v is not None, "value must not be None for alerts with handle_type='state'"
        return v
