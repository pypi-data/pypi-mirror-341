# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Health = Literal["fair", "good", "n/a", "poor"]

State = Literal["Down", "Up"]


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
class TunnelHealthData:
    jitter: Optional[int] = _field(default=None)
    latency: Optional[int] = _field(default=None)
    loss_percentage: Optional[int] = _field(default=None)
    rx_octets: Optional[int] = _field(default=None)
    state: Optional[State] = _field(default=None)
    tx_octets: Optional[int] = _field(default=None)
    vqoe_score: Optional[int] = _field(default=None)


@dataclass
class TunnelHealthHistoryItem:
    health: Optional[Health] = _field(default=None)
    health_score: Optional[int] = _field(default=None)
    history: Optional[List[DeviceHealthEntryItem]] = _field(default=None)
    local_color: Optional[str] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    remote_color: Optional[str] = _field(default=None)
    remote_system_ip: Optional[str] = _field(default=None)
    summary: Optional[TunnelHealthData] = _field(default=None)
