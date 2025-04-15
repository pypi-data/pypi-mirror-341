# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class VnicInfo:
    deployment_name: Optional[str] = _field(default=None, metadata={"alias": "deploymentName"})
    network: Optional[str] = _field(default=None)
    nic_id: Optional[str] = _field(default=None, metadata={"alias": "nicId"})
    vm_group_name: Optional[str] = _field(default=None, metadata={"alias": "vmGroupName"})
