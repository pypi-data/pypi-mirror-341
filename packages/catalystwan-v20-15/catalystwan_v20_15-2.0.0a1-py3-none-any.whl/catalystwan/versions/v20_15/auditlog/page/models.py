# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AuditLogEntry:
    auditdetails: List[str]
    entry_time: int
    logdeviceid: str
    logfeature: str
    logid: str
    logmessage: str
    logmodule: str
    loguser: str
    logusersrcip: str
    statcycletime: int
    tenant: str
    id: Optional[str] = _field(default=None)


@dataclass
class ChartObject:
    series: Optional[List[str]] = _field(default=None)
    title: Optional[str] = _field(default=None)
    x_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "xAxis"})
    x_axis_label: Optional[str] = _field(default=None, metadata={"alias": "xAxisLabel"})
    y_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "yAxis"})
    y_axis_label: Optional[str] = _field(default=None, metadata={"alias": "yAxisLabel"})


@dataclass
class AuditLogHeaderColumns:
    data_type: str = _field(metadata={"alias": "dataType"})
    property: str
    title: str
    display_format: Optional[str] = _field(default=None, metadata={"alias": "displayFormat"})
    hideable: Optional[bool] = _field(default=None)
    input_format: Optional[str] = _field(default=None, metadata={"alias": "inputFormat"})
    is_display: Optional[bool] = _field(default=None, metadata={"alias": "isDisplay"})
    min_width: Optional[int] = _field(default=None, metadata={"alias": "minWidth"})
    width: Optional[int] = _field(default=None)


@dataclass
class GetStatDataFields:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)


@dataclass
class AuditLogHeaderViewKeys:
    preference_key: Optional[str] = _field(default=None, metadata={"alias": "preferenceKey"})
    unique_key: Optional[List[str]] = _field(default=None, metadata={"alias": "uniqueKey"})


@dataclass
class AuditLogHeader:
    chart: Optional[ChartObject] = _field(default=None)
    columns: Optional[AuditLogHeaderColumns] = _field(default=None)
    fields: Optional[GetStatDataFields] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[AuditLogHeaderViewKeys] = _field(
        default=None, metadata={"alias": "viewKeys"}
    )


@dataclass
class GetAuditLogData:
    data: List[AuditLogEntry]
    header: AuditLogHeader
