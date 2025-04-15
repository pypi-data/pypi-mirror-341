# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FirmwareImageRemoteUpgradeDevices:
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIP"})


@dataclass
class FirmwareImageRemoteUpgradeInputData:
    family: Optional[str] = _field(default=None)
    remote_server_id: Optional[str] = _field(default=None, metadata={"alias": "remoteServerId"})
    version: Optional[str] = _field(default=None)


@dataclass
class FirmwareImageRemoteUpgradeInput:
    data: Optional[List[FirmwareImageRemoteUpgradeInputData]] = _field(default=None)
    version_type: Optional[str] = _field(default=None, metadata={"alias": "versionType"})


@dataclass
class FirmwareImageRemoteUpgrade:
    action: Optional[str] = _field(default=None)
    action_end: Optional[str] = _field(default=None, metadata={"alias": "actionEnd"})
    action_end_millis: Optional[int] = _field(default=None, metadata={"alias": "actionEndMillis"})
    action_name: Optional[str] = _field(default=None, metadata={"alias": "actionName"})
    action_start: Optional[str] = _field(default=None, metadata={"alias": "actionStart"})
    action_start_millis: Optional[int] = _field(
        default=None, metadata={"alias": "actionStartMillis"}
    )
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    devices: Optional[List[FirmwareImageRemoteUpgradeDevices]] = _field(default=None)
    input: Optional[FirmwareImageRemoteUpgradeInput] = _field(default=None)
    time_zone: Optional[str] = _field(default=None, metadata={"alias": "timeZone"})
