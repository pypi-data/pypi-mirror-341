# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class WcmNetconfConfigRes:
    id: Optional[str] = _field(default=None)


@dataclass
class NetconfConfig:
    device_config: Optional[str] = _field(default=None, metadata={"alias": "deviceConfig"})
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})


@dataclass
class NetconfConfigHeader:
    generate_on: Optional[int] = _field(default=None, metadata={"alias": "generateOn"})


@dataclass
class WcmNetconfConfigRequest:
    data: Optional[List[NetconfConfig]] = _field(default=None)
    header: Optional[NetconfConfigHeader] = _field(default=None)
