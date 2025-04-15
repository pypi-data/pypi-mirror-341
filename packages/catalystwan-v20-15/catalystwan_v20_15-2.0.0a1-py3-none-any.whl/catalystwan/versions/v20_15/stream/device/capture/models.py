# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

RequestStatus = Literal["IN_PROGRESS", "NOT_STARTED", "START", "STOP"]

Status = Literal["failure", "success"]

Type = Literal["control", "data"]


@dataclass
class PacketCaptureInfo:
    _rid: Optional[int] = _field(default=None, metadata={"alias": "@rid"})
    is_new_session: Optional[bool] = _field(default=None, metadata={"alias": "isNewSession"})
    is_owner: Optional[bool] = _field(default=None, metadata={"alias": "isOwner"})
    j_session_id: Optional[str] = _field(default=None, metadata={"alias": "JSessionId"})
    renewal_time: Optional[int] = _field(default=None, metadata={"alias": "renewalTime"})
    request_status: Optional[RequestStatus] = _field(
        default=None, metadata={"alias": "requestStatus"}
    )
    session_id: Optional[str] = _field(default=None, metadata={"alias": "sessionId"})
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})
    status: Optional[Status] = _field(default=None)
    status_message: Optional[str] = _field(default=None, metadata={"alias": "statusMessage"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    user: Optional[str] = _field(default=None)
    user_ip: Optional[str] = _field(default=None, metadata={"alias": "userIp"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class CreatePacketCaptureReq:
    bidirectional: Optional[bool] = _field(default=None)
    destination_ip: Optional[str] = _field(default=None)
    destination_port: Optional[str] = _field(default=None)
    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUUID"})
    interface: Optional[str] = _field(default=None)
    interface_ip: Optional[str] = _field(default=None, metadata={"alias": "interfaceIP"})
    protocol: Optional[str] = _field(default=None)
    source_ip: Optional[str] = _field(default=None)
    source_port: Optional[str] = _field(default=None)
    type_: Optional[Type] = _field(default=None, metadata={"alias": "type"})
    vpn: Optional[str] = _field(default=None)


@dataclass
class FormPacketCaptureRes:
    status: Optional[str] = _field(default=None)
