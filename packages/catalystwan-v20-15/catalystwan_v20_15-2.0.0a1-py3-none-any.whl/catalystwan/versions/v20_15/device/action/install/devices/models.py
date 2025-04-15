# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GenerateDeviceListData:
    available_versions: Optional[List[str]] = _field(
        default=None, metadata={"alias": "availableVersions"}
    )
    current_partition: Optional[str] = _field(default=None, metadata={"alias": "current-partition"})
    default_version: Optional[str] = _field(default=None, metadata={"alias": "defaultVersion"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_os: Optional[str] = _field(default=None, metadata={"alias": "device-os"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    is_multi_step_upgrade_supported: Optional[bool] = _field(
        default=None, metadata={"alias": "isMultiStepUpgradeSupported"}
    )
    is_schedule_upgrade_supported: Optional[bool] = _field(
        default=None, metadata={"alias": "isScheduleUpgradeSupported"}
    )
    layout_level: Optional[int] = _field(default=None, metadata={"alias": "layoutLevel"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    platform_family: Optional[str] = _field(default=None, metadata={"alias": "platformFamily"})
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)


@dataclass
class GenerateDeviceList:
    data: Optional[List[GenerateDeviceListData]] = _field(default=None)
