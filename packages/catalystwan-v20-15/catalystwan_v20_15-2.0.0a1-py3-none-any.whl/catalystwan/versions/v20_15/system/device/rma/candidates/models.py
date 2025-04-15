# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class GetRmaCandidates:
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIP"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    management_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "managementSystemIP"}
    )
    uuid: Optional[str] = _field(default=None)
    validity: Optional[str] = _field(default=None)
