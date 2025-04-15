# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FlowlogAggreation:
    count: Optional[int] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)


@dataclass
class FlowlogAggregationResponseHeaderColumns:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    is_display: Optional[bool] = _field(default=None, metadata={"alias": "isDisplay"})
    property: Optional[str] = _field(default=None)
    title: Optional[str] = _field(default=None)


@dataclass
class FlowlogAggregationResponseHeaderFields:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)


@dataclass
class FlowlogAggregationResponseHeader:
    columns: Optional[List[FlowlogAggregationResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[FlowlogAggregationResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class FlowlogAggregationResponse:
    data: Optional[FlowlogAggreation] = _field(default=None)
    entry_time_list: Optional[List[int]] = _field(default=None, metadata={"alias": "entryTimeList"})
    header: Optional[FlowlogAggregationResponseHeader] = _field(default=None)
