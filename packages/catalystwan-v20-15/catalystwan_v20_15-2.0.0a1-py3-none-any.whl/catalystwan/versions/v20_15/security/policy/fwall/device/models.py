# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceLists:
    entry_time: int
    device_ip: Optional[str] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    site_name: Optional[str] = _field(default=None)
