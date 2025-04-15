# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AppRouteAggResp:
    count: Optional[int] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    local_color: Optional[str] = _field(default=None)
    loss_percentage: Optional[int] = _field(default=None)


@dataclass
class PageInfo:
    # number of alarms to be fetched
    count: Optional[int] = _field(default=None)
    # end time of alarms to be fetched
    end_time: Optional[int] = _field(default=None, metadata={"alias": "endTime"})
    # start time of alarms to be fetched
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class AppRouteAggRespWithPageInfo:
    """
    interface aggregation response with page info
    """

    data: Optional[List[AppRouteAggResp]] = _field(default=None)
    page_info: Optional[PageInfo] = _field(default=None, metadata={"alias": "pageInfo"})
