# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GenerateRemovePartitionInfoData:
    available_versions: Optional[List[str]] = _field(
        default=None, metadata={"alias": "availableVersions"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[str] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)


@dataclass
class GenerateRemovePartitionInfo:
    data: Optional[List[GenerateRemovePartitionInfoData]] = _field(default=None)


@dataclass
class DeviceIp:
    """
    This is the valid DeviceIP
    """

    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIp"})
