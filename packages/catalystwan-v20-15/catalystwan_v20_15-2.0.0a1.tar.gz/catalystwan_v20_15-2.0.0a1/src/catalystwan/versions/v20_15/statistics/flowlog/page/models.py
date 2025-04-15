# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FlowlogDataObject:
    action: Optional[str] = _field(default=None)
    dest_ip: Optional[str] = _field(default=None)
    dest_port: Optional[int] = _field(default=None)
    device_model: Optional[str] = _field(default=None)
    direction: Optional[str] = _field(default=None)
    dscp: Optional[int] = _field(default=None)
    egress_intf: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    flow_active: Optional[str] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    ingress_intf: Optional[str] = _field(default=None)
    ip_proto: Optional[int] = _field(default=None)
    policy_name: Optional[str] = _field(default=None)
    src_ip: Optional[str] = _field(default=None)
    src_port: Optional[int] = _field(default=None)
    start_time: Optional[int] = _field(default=None)
    statcycletime: Optional[int] = _field(default=None)
    stats_data_id: Optional[str] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    total_bytes: Optional[int] = _field(default=None)
    total_pkts: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
    vmanage_system_ip: Optional[str] = _field(default=None)
    vpn_id: Optional[int] = _field(default=None)


@dataclass
class FlowlogPaginationResponsePageInfo:
    count: Optional[int] = _field(default=None)
    end_time: Optional[str] = _field(default=None, metadata={"alias": "endTime"})
    has_more_data: Optional[str] = _field(default=None, metadata={"alias": "hasMoreData"})
    scroll_id: Optional[str] = _field(default=None, metadata={"alias": "scrollId"})
    start_time: Optional[str] = _field(default=None, metadata={"alias": "startTime"})
    total_count: Optional[int] = _field(default=None, metadata={"alias": "totalCount"})


@dataclass
class FlowlogPaginationResponse:
    data: Optional[List[FlowlogDataObject]] = _field(default=None)
    page_info: Optional[FlowlogPaginationResponsePageInfo] = _field(
        default=None, metadata={"alias": "pageInfo"}
    )
