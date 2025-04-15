# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceAppDetailResponseData:
    application: Optional[str] = _field(default=None)
    create_time: Optional[int] = _field(default=None)
    dest_ip: Optional[str] = _field(default=None)
    dest_port: Optional[int] = _field(default=None)
    device_model: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None)
    family: Optional[str] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    ip_proto: Optional[int] = _field(default=None)
    octets: Optional[int] = _field(default=None)
    packets: Optional[int] = _field(default=None)
    source_ip: Optional[str] = _field(default=None)
    source_port: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
    vip_idx: Optional[int] = _field(default=None)
    vpn_id: Optional[int] = _field(default=None)


@dataclass
class DeviceAppDetailResponseHeaderChart:
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
class DeviceAppDetailResponseHeaderViewKeys:
    preference_key: Optional[str] = _field(default=None, metadata={"alias": "preferenceKey"})
    unique_key: Optional[List[str]] = _field(default=None, metadata={"alias": "uniqueKey"})


@dataclass
class DeviceAppDetailResponseHeader:
    chart: Optional[DeviceAppDetailResponseHeaderChart] = _field(default=None)
    columns: Optional[List[DeviceAppResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[DeviceAppResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[DeviceAppDetailResponseHeaderViewKeys] = _field(
        default=None, metadata={"alias": "viewKeys"}
    )


@dataclass
class DeviceAppDetailResponsePageInfo:
    count: Optional[int] = _field(default=None)
    end_time: Optional[str] = _field(default=None, metadata={"alias": "endTime"})
    start_time: Optional[str] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class DeviceAppDetailResponse:
    data: Optional[List[DeviceAppDetailResponseData]] = _field(default=None)
    header: Optional[DeviceAppDetailResponseHeader] = _field(default=None)
    page_info: Optional[DeviceAppDetailResponsePageInfo] = _field(
        default=None, metadata={"alias": "pageInfo"}
    )
