# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceInfoResponsePayloadDataDevices:
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    latitude: Optional[str] = _field(default=None)
    layout_level: Optional[int] = _field(default=None, metadata={"alias": "layoutLevel"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    longitude: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)


@dataclass
class DeviceInfoResponsePayloadDataInterfaces:
    ifname: Optional[str] = _field(default=None)
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ip-address"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})


@dataclass
class DeviceInfoResponsePayloadDataModels:
    device_class: Optional[str] = _field(default=None, metadata={"alias": "deviceClass"})
    name: Optional[str] = _field(default=None)


@dataclass
class DeviceInfoResponsePayloadData:
    devices: Optional[List[DeviceInfoResponsePayloadDataDevices]] = _field(default=None)
    interfaces: Optional[List[DeviceInfoResponsePayloadDataInterfaces]] = _field(default=None)
    models: Optional[List[DeviceInfoResponsePayloadDataModels]] = _field(default=None)
