# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class VedgeInventoryData:
    chasis_number: Optional[str] = _field(default=None, metadata={"alias": "chasisNumber"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    serial_number: Optional[str] = _field(default=None, metadata={"alias": "serialNumber"})
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    validity: Optional[str] = _field(default=None)
