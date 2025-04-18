from typing import Dict, Optional

from openmodule.models.base import ZMQMessage, Gateway, OpenModuleModel, Datetime


class IoMessage(ZMQMessage):
    gateway: Gateway
    type: str
    pin: str
    value: int
    inverted: bool = False
    physical: Optional[int] = None
    edge: int
    pin_number: Optional[int] = None
    pin_label: Optional[str] = None
    meta: Dict = {}


class IoState(OpenModuleModel):
    gateway: Gateway
    type: str
    pin: str
    value: int
    inverted: bool
    physical: int
    last_timestamp: Datetime
