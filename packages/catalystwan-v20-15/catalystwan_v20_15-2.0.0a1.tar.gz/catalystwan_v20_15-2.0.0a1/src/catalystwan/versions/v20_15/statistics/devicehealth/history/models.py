# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Health = Literal["fair", "good", "n/a", "poor"]


@dataclass
class DeviceHealthEntryItem:
    cpu_load: Optional[int] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    health: Optional[Health] = _field(default=None)
    health_score: Optional[int] = _field(default=None)
    memory_utilization: Optional[int] = _field(default=None)
    qoe: Optional[int] = _field(default=None)
    reachability: Optional[str] = _field(default=None)


@dataclass
class DeviceHealthHistoryItem:
    cpu_load: Optional[int] = _field(default=None)
    health: Optional[Health] = _field(default=None)
    health_score: Optional[int] = _field(default=None)
    history: Optional[List[DeviceHealthEntryItem]] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    memory_utilization: Optional[int] = _field(default=None)
    qoe: Optional[int] = _field(default=None)
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
