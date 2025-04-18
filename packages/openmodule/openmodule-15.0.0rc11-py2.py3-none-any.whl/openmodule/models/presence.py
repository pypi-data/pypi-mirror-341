import datetime
from typing import Optional, List

from pydantic import ConfigDict, Field, model_validator

from openmodule.models.base import ZMQMessage, OpenModuleModel, Gateway, Datetime
from openmodule.models.vehicle import Medium, LPRMedium, MakeModel, PresenceAllIds, EnterDirection, QRMedium


class PresenceMedia(OpenModuleModel):
    lpr: Optional[LPRMedium] = None
    qr: Optional[QRMedium] = None
    nfc: Optional[Medium] = None
    pin: Optional[Medium] = None


class PresenceBaseData(OpenModuleModel):
    vehicle_id: int
    source: str
    present_area_name: str = Field(..., alias="present-area-name")
    last_update: Datetime
    gateway: Gateway
    medium: PresenceMedia
    make_model: Optional[MakeModel] = None
    all_ids: PresenceAllIds
    enter_direction: EnterDirection = EnterDirection.unknown
    enter_time: Datetime

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    @model_validator(mode="before")
    def set_enter_time_default(cls, values_dict: dict) -> dict:
        """for backward compatibility, set enter_time based on vehicle_id"""
        if values_dict.get("enter_time") is None:
            utc_datetime = datetime.datetime.fromtimestamp(values_dict["vehicle_id"] / 1e9, datetime.timezone.utc)
            values_dict["enter_time"] = utc_datetime  # timestamp from vehicle_id
        return values_dict


class PresenceBaseMessage(PresenceBaseData, ZMQMessage):
    pass


class PresenceBackwardMessage(PresenceBaseMessage):
    type: str = "backward"
    unsure: bool = False
    leave_time: Datetime = Field(..., alias="leave-time")
    bidirectional_inverse: bool = False


class PresenceForwardMessage(PresenceBaseMessage):
    type: str = "forward"
    unsure: bool = False
    leave_time: Datetime = Field(..., alias="leave-time")
    bidirectional_inverse: bool = False


class PresenceLeaveMessage(PresenceBaseMessage):
    type: str = "leave"
    num_presents: int = Field(0, alias="num-presents")
    leave_time: Datetime = Field(..., alias="leave-time")

    @model_validator(mode="before")
    def set_leave_time_default(cls, values_dict: dict) -> dict:
        if values_dict.get("leave_time") is None:
            values_dict["leave_time"] = values_dict["timestamp"]  # timestamp from message timestamp
        return values_dict


class PresenceEnterMessage(PresenceBaseMessage):
    type: str = "enter"


class PresenceChangeMessage(PresenceBaseMessage):
    type: str = "change"
    change_vehicle_id: Optional[bool] = None


class PresenceRPCRequest(OpenModuleModel):
    gate: str


class PresenceRPCResponse(OpenModuleModel):
    presents: List[PresenceBaseData]
