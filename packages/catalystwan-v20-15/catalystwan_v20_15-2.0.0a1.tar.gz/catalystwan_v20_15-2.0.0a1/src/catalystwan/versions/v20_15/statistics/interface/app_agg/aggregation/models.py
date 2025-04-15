# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterfaceAggResp:
    count: Optional[int] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    rx_kbps: Optional[int] = _field(default=None)
    tx_kbps: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
