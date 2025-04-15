# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SpeedTestInterfaceResponse:
    """
    This is valid speedTestInterfaceResponse
    """

    down_bw: Optional[str] = _field(default=None)
    up_bw: Optional[str] = _field(default=None)


@dataclass
class DeviceUuid:
    """
    This is valid DeviceUuid
    """

    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUuid"})
