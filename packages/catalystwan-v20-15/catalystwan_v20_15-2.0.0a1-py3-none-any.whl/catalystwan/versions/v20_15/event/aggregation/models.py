# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Severity = Literal["CRITICAL", "MAJOR", "MEDIUM", "MINOR"]


@dataclass
class AlarmAggregation:
    count: Optional[int] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    severity: Optional[Severity] = _field(default=None)


@dataclass
class AlarmAggregationResponse:
    data: Optional[AlarmAggregation] = _field(default=None)
    entry_time_list: Optional[List[int]] = _field(default=None, metadata={"alias": "entryTimeList"})
