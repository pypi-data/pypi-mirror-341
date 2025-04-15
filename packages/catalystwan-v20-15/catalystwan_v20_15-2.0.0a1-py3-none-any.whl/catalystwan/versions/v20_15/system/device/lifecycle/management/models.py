# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SetLifeCycle:
    device_life_cycle_needed: Optional[bool] = _field(
        default=None, metadata={"alias": "DeviceLifeCycleNeeded"}
    )
