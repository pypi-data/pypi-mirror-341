# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

HealthParam = Literal["FAIR", "GOOD", "POOR"]


@dataclass
class ApplicationSiteItem:
    health: str
    jitter: int
    latency: int
    loss: int
    path: str
    qoe: Optional[int] = _field(default=None)
