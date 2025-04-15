# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceCountersData:
    crash_count: Optional[int] = _field(default=None, metadata={"alias": "crashCount"})
    expected_control_connections: Optional[int] = _field(
        default=None, metadata={"alias": "expectedControlConnections"}
    )
    number_vsmart_control_connections: Optional[int] = _field(
        default=None, metadata={"alias": "number-vsmart-control-connections"}
    )
    reboot_count: Optional[int] = _field(default=None, metadata={"alias": "rebootCount"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})


@dataclass
class DeviceResponseHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class DeviceCountersResponse:
    data: Optional[List[DeviceCountersData]] = _field(default=None)
    header: Optional[DeviceResponseHeader] = _field(default=None)
