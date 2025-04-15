# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SimpleKeyValueMapping:
    key: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class AlarmSeverityMapping:
    associated_alarms: Optional[List[SimpleKeyValueMapping]] = _field(
        default=None, metadata={"alias": "associatedAlarms"}
    )
    key: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)
