# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AppRouteTunnelSummary:
    app_probe_class: Optional[str] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    jitter: Optional[int] = _field(default=None)
    latency: Optional[int] = _field(default=None)
    loss_percentage: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    rx_octets: Optional[int] = _field(default=None)
    tx_octets: Optional[int] = _field(default=None)


@dataclass
class AppRouteTunnenSummarResp:
    data: Optional[List[AppRouteTunnelSummary]] = _field(default=None)
