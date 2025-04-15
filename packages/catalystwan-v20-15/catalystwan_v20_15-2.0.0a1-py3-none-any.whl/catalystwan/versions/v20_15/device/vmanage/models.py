# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceVmanageResponseData:
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ipAddress"})


@dataclass
class DeviceResponseHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class DeviceVmanageResponse:
    data: Optional[DeviceVmanageResponseData] = _field(default=None)
    header: Optional[DeviceResponseHeader] = _field(default=None)
