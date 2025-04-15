# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class UrlMonitoringInfoInner:
    alarm_raised: Optional[bool] = _field(default=None, metadata={"alias": "alarmRaised"})
    # VManage alarm is raised after reaching the threshold.
    threshold: Optional[int] = _field(default=None)
    # url registered for monitoring requests.
    url: Optional[str] = _field(default=None)
