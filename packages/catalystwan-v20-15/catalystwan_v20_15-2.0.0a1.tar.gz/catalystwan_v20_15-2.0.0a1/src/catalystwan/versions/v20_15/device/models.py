# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceData:
    board_serial: Optional[str] = _field(default=None, metadata={"alias": "board-serial"})
    certificate_validity: Optional[str] = _field(
        default=None, metadata={"alias": "certificate-validity"}
    )
    connected_v_manages: Optional[List[str]] = _field(
        default=None, metadata={"alias": "connectedVManages"}
    )
    control_connections: Optional[str] = _field(
        default=None, metadata={"alias": "controlConnections"}
    )
    device_groups: Optional[List[str]] = _field(default=None, metadata={"alias": "device-groups"})
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_os: Optional[str] = _field(default=None, metadata={"alias": "device-os"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    domain_id: Optional[str] = _field(default=None, metadata={"alias": "domain-id"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    is_device_geo_data: Optional[bool] = _field(default=None, metadata={"alias": "isDeviceGeoData"})
    lastupdated: Optional[str] = _field(default=None)
    latitude: Optional[str] = _field(default=None)
    layout_level: Optional[int] = _field(default=None, metadata={"alias": "layoutLevel"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    longitude: Optional[str] = _field(default=None)
    max_controllers: Optional[str] = _field(default=None, metadata={"alias": "max-controllers"})
    model_sku: Optional[str] = _field(default=None)
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    state: Optional[str] = _field(default=None)
    state_description: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    status_order: Optional[str] = _field(default=None, metadata={"alias": "statusOrder"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    testbed_mode: Optional[bool] = _field(default=None)
    timezone: Optional[str] = _field(default=None)
    total_cpu_count: Optional[str] = _field(default=None)
    uptime_date: Optional[str] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    validity: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
