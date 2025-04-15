# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterconnectService:
    # Virtual Instance flavor of the service instance
    flavor: Optional[str] = _field(default=None)
    # Number of interfaces for the service
    interface_count: Optional[str] = _field(default=None, metadata={"alias": "interfaceCount"})
    # IP of the management interface of the service
    mgmt_ip: Optional[str] = _field(default=None, metadata={"alias": "mgmtIP"})
    # Name of the service
    name: Optional[str] = _field(default=None)
    # Region where the service is deployed
    service_region: Optional[str] = _field(default=None, metadata={"alias": "serviceRegion"})
    # HA role of the service
    service_role: Optional[str] = _field(default=None, metadata={"alias": "serviceRole"})
    # Status of the service
    status: Optional[str] = _field(default=None)
    # Software version running on the service
    sw_version: Optional[str] = _field(default=None, metadata={"alias": "swVersion"})
    # provider assigned service Uuid
    uuid: Optional[str] = _field(default=None)
