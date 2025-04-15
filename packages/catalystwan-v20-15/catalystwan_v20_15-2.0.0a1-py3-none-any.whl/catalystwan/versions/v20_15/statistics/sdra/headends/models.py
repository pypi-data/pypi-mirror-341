# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SdraHeadendSummary:
    ipsec_enabled: Optional[int] = _field(default=None)
    sslvpn_enabled: Optional[int] = _field(default=None)
