# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeployPolicyGroupPostResponse:
    """
    Policy Group deploy Response schema
    """

    parent_task_id: str = _field(metadata={"alias": "parentTaskId"})


@dataclass
class DeviceIdDef:
    id: str


@dataclass
class DeployPolicyGroupPostRequest:
    """
    Policy Group Deploy Request schema
    """

    # list of device ids that policy group need to be deployed
    devices: Optional[List[DeviceIdDef]] = _field(default=None)
