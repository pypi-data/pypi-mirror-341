# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceDetails:
    """
    Device list to onboard
    """

    # host ip
    host: str
    # ssh password
    password: str
    # ssh username
    username: str
    # WAN interface name
    wan: str
    # device uuid/chassis number
    device_uuid: Optional[str] = _field(default=None)
    # enable password
    enable_password: Optional[str] = _field(default=None)
    # local file name
    local_file_name: Optional[str] = _field(default=None)
    # remote server file name
    remote_server_file_name: Optional[str] = _field(default=None)
    # remote server Id
    remote_server_id: Optional[str] = _field(default=None)


@dataclass
class DeviceDetailsData:
    # Device list to onboard
    devices: List[DeviceDetails]
