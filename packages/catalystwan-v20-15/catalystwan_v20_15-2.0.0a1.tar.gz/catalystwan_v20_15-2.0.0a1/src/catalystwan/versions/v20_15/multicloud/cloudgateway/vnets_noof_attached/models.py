# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class IsVnetAttached:
    is_vnet_attached: Optional[bool] = _field(default=None, metadata={"alias": "isVnetAttached"})
