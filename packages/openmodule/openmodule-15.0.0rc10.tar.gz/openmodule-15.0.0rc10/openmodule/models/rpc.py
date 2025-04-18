from enum import StrEnum
from typing import Optional, Dict, Any
from uuid import UUID

from openmodule.models.base import ZMQMessage, OpenModuleModel


class RPCRequest(ZMQMessage):
    rpc_id: UUID
    resource: Optional[str] = None
    request: Optional[Dict] = None


class RPCResponse(ZMQMessage):
    rpc_id: Optional[UUID] = None
    response: Optional[Any] = None


class RPCServerError(StrEnum):
    handler_error = "handler_error"
    validation_error = "validation_error"
    filter_error = "filter_error"
    error = "error"  # this is from RPCServer (the WebServer, not an RPCServer on the device)


class RPCErrorResult(OpenModuleModel):
    status: RPCServerError
    error: Optional[str] = None
    exception: Optional[Any] = None


class ServerRPCRequest(OpenModuleModel):
    rpc: str
    data: Optional[Any] = None
