# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SupportedResponseUuid:
    device_mødel: Optional[str] = _field(default=None, metadata={"alias": "deviceMødel"})
    is_autonomous_supported: Optional[bool] = _field(
        default=None, metadata={"alias": "isAutonomousSupported"}
    )
    is_software_device: Optional[bool] = _field(
        default=None, metadata={"alias": "isSoftwareDevice"}
    )
    is_system_ip_pool_needed: Optional[bool] = _field(
        default=None, metadata={"alias": "isSystemIpPoolNeeded"}
    )


@dataclass
class SupportedResponse:
    uuid: Optional[SupportedResponseUuid] = _field(default=None)
