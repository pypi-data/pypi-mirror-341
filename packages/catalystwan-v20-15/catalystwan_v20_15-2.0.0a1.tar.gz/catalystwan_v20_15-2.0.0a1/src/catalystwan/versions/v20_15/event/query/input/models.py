# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SimpleKeyValueMapping:
    key: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class TimeOptions:
    enable_date_fields: Optional[bool] = _field(
        default=None, metadata={"alias": "enableDateFields"}
    )
    key: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class EventQueryInputResponse:
    component: Optional[List[SimpleKeyValueMapping]] = _field(default=None)
    severity_options: Optional[List[SimpleKeyValueMapping]] = _field(
        default=None, metadata={"alias": "severityOptions"}
    )
    time_options: Optional[List[TimeOptions]] = _field(
        default=None, metadata={"alias": "timeOptions"}
    )
