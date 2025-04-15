# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class VwanListResponse:
    source: Optional[str] = _field(default=None)
    vwan_id: Optional[str] = _field(default=None, metadata={"alias": "vwanId"})
    vwan_name: Optional[str] = _field(default=None, metadata={"alias": "vwanName"})
