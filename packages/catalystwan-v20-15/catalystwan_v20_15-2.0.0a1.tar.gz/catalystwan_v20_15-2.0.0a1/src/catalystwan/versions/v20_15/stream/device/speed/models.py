# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SpeedTestResponse:
    """
    This is valid speedTestResponse
    """

    is_new_session: Optional[bool] = _field(default=None, metadata={"alias": "isNewSession"})
    is_owner: Optional[bool] = _field(default=None, metadata={"alias": "isOwner"})
    renewal_time: Optional[int] = _field(default=None, metadata={"alias": "renewalTime"})
    session_id: Optional[str] = _field(default=None, metadata={"alias": "sessionId"})
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    user_ip: Optional[str] = _field(default=None, metadata={"alias": "userIp"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class ServerList:
    server_name: Optional[str] = _field(default=None, metadata={"alias": "server-name"})
    server_ports: Optional[str] = _field(default=None, metadata={"alias": "server-ports"})


@dataclass
class SpeedTestSession:
    """
    This is valid SpeedTestSession
    """

    destination_color: Optional[str] = _field(default=None, metadata={"alias": "destinationColor"})
    destination_ip: Optional[str] = _field(default=None, metadata={"alias": "destinationIp"})
    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUUID"})
    port: Optional[str] = _field(default=None)
    server_list: Optional[List[ServerList]] = _field(
        default=None, metadata={"alias": "server-list"}
    )
    source_color: Optional[str] = _field(default=None, metadata={"alias": "sourceColor"})
    source_interface: Optional[str] = _field(default=None, metadata={"alias": "sourceInterface"})
    source_ip: Optional[str] = _field(default=None, metadata={"alias": "sourceIp"})


@dataclass
class SpeedTestStatusResponse:
    """
    This is valid speedTestStatusResponse
    """

    status: Optional[str] = _field(default=None)


@dataclass
class Uuid:
    """
    This is valid uuid
    """

    uuid: Optional[str] = _field(default=None)


@dataclass
class SpeedTestResult:
    """
    This is valid SpeedTestResult
    """

    down_speed: Optional[int] = _field(default=None, metadata={"alias": "down-speed"})
    error: Optional[str] = _field(default=None)
    location: Optional[str] = _field(default=None)
    server: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    up_speed: Optional[int] = _field(default=None, metadata={"alias": "up-speed"})


@dataclass
class SpeedTestData:
    """
    This is valid speedTestData
    """

    destination_circuit: Optional[str] = _field(default=None)
    destination_ip: Optional[str] = _field(default=None)
    destination_local_ip: Optional[str] = _field(default=None)
    device_uuid: Optional[str] = _field(default=None)
    down_bw: Optional[str] = _field(default=None)
    down_speed: Optional[int] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    error: Optional[str] = _field(default=None)
    logid: Optional[int] = _field(default=None)
    port: Optional[str] = _field(default=None)
    session_id: Optional[str] = _field(default=None)
    source_circuit: Optional[str] = _field(default=None)
    source_ip: Optional[str] = _field(default=None)
    source_local_ip: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    up_bw: Optional[str] = _field(default=None)
    up_speed: Optional[int] = _field(default=None)


@dataclass
class SpeedTestResultResponse:
    """
    This is valid speedTestResultResponse
    """

    # This is valid speedTestData
    data: Optional[SpeedTestData] = _field(default=None)
