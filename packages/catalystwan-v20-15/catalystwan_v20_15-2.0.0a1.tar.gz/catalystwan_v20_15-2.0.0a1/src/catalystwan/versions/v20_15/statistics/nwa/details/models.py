# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

Health = Literal["fair", "good", "poor"]


@dataclass
class NetworkAvailabilityResp:
    health: Health  # pytype: disable=annotation-type-mismatch
    jitter: int
    latency: int
    loss: int
    availability: Optional[int] = _field(default=None)
    latitude: Optional[str] = _field(default=None)
    longitude: Optional[str] = _field(default=None)
    siteid: Optional[str] = _field(default=None)
    sitename: Optional[str] = _field(default=None)
