# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceAppResponseData:
    octets: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)


@dataclass
class DeviceAppResponseHeaderChart:
    series: Optional[List[str]] = _field(default=None)
    title: Optional[str] = _field(default=None)
    x_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "xAxis"})
    x_axis_label: Optional[str] = _field(default=None, metadata={"alias": "xAxisLabel"})
    y_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "yAxis"})
    y_axis_label: Optional[str] = _field(default=None, metadata={"alias": "yAxisLabel"})


@dataclass
class DeviceAppResponseHeaderColumns:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)
    title: Optional[str] = _field(default=None)


@dataclass
class DeviceAppResponseHeaderFields:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)


@dataclass
class DeviceAppResponseHeaderViewKeys:
    preference_key: Optional[str] = _field(default=None, metadata={"alias": "preferenceKey"})
    unique_key: Optional[List[str]] = _field(default=None, metadata={"alias": "uniqueKey"})


@dataclass
class DeviceAppResponseHeader:
    chart: Optional[DeviceAppResponseHeaderChart] = _field(default=None)
    columns: Optional[List[DeviceAppResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[DeviceAppResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[DeviceAppResponseHeaderViewKeys] = _field(
        default=None, metadata={"alias": "viewKeys"}
    )


@dataclass
class DeviceAppResponse:
    data: Optional[List[DeviceAppResponseData]] = _field(default=None)
    header: Optional[DeviceAppResponseHeader] = _field(default=None)
