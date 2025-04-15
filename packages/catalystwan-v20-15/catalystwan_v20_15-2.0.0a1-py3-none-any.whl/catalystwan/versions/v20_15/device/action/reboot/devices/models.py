# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GenerateRebootDeviceListData:
    available_services: Optional[List[str]] = _field(
        default=None, metadata={"alias": "availableServices"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_os: Optional[str] = _field(default=None, metadata={"alias": "device-os"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    layout_level: Optional[int] = _field(default=None, metadata={"alias": "layoutLevel"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)


@dataclass
class GenerateRebootDeviceList:
    data: Optional[List[GenerateRebootDeviceListData]] = _field(default=None)
