# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class CapacityRespData:
    avg_down_capacity_percentage: Optional[int] = _field(default=None)
    avg_up_capacity_percentage: Optional[int] = _field(default=None)
    bw_down: Optional[int] = _field(default=None)
    bw_up: Optional[int] = _field(default=None)
    count: Optional[int] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    max_down_capacity_percentage: Optional[int] = _field(default=None)
    max_up_capacity_percentage: Optional[int] = _field(default=None)
    min_down_capacity_percentage: Optional[int] = _field(default=None)
    min_up_capacity_percentage: Optional[int] = _field(default=None)
    range: Optional[str] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)


@dataclass
class CapDistribution:
    s_0_25: Optional[int] = _field(default=None, metadata={"alias": "0-25"})
    s_100: Optional[int] = _field(default=None, metadata={"alias": "100"})
    s_25_50: Optional[int] = _field(default=None, metadata={"alias": "25-50"})
    s_50_75: Optional[int] = _field(default=None, metadata={"alias": "50-75"})
    s_75_100: Optional[int] = _field(default=None, metadata={"alias": "75-100"})
    uncategorized: Optional[int] = _field(default=None)


@dataclass
class CapacityResp:
    data: Optional[List[CapacityRespData]] = _field(default=None)
    distribution: Optional[CapDistribution] = _field(default=None)
