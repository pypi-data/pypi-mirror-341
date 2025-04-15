# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AppRouteTransportResp:
    app_probe_class: Optional[str] = _field(default=None)
    color: Optional[str] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    jitter: Optional[str] = _field(default=None)
    latency: Optional[int] = _field(default=None)
    loss_percentage: Optional[int] = _field(default=None)
