# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class TraceCftRecordResponsePayloadData:
    agg_total_bytes: Optional[int] = _field(default=None)
    agg_total_fif_bytes: Optional[int] = _field(default=None)
    agg_total_fif_packets: Optional[int] = _field(default=None)
    agg_total_fin_flows: Optional[int] = _field(default=None)
    agg_total_flows: Optional[int] = _field(default=None)
    agg_total_packets: Optional[int] = _field(default=None)
    agg_total_ttl_ms: Optional[int] = _field(default=None)
    app_group: Optional[str] = _field(default=None)
    app_name: Optional[str] = _field(default=None)
    avg_bps: Optional[int] = _field(default=None)
    avg_concurrent_flows: Optional[int] = _field(default=None)
    avg_cps: Optional[int] = _field(default=None)
    avg_pps: Optional[int] = _field(default=None)
    avg_ttl_ms: Optional[int] = _field(default=None)
    bps: Optional[int] = _field(default=None)
    concurrent_flows: Optional[int] = _field(default=None)
    cps: Optional[int] = _field(default=None)
    device_name: Optional[str] = _field(default=None)
    device_trace_id: Optional[int] = _field(default=None)
    device_uuid: Optional[str] = _field(default=None)
    if_name: Optional[str] = _field(default=None)
    last_report_ts: Optional[int] = _field(default=None)
    local_color: Optional[str] = _field(default=None)
    max_bps: Optional[int] = _field(default=None)
    max_concurrent_flows: Optional[int] = _field(default=None)
    max_cps: Optional[int] = _field(default=None)
    max_pps: Optional[int] = _field(default=None)
    max_ttl_ms: Optional[int] = _field(default=None)
    min_bps: Optional[int] = _field(default=None)
    min_concurrent_flows: Optional[int] = _field(default=None)
    min_cps: Optional[int] = _field(default=None)
    min_pps: Optional[int] = _field(default=None)
    min_ttl_ms: Optional[int] = _field(default=None)
    model: Optional[str] = _field(default=None)
    pps: Optional[int] = _field(default=None)
    received_timestamp: Optional[int] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None)


@dataclass
class TraceCftRecordResponsePayload:
    """
    Get cft record for GET response
    """

    data: Optional[TraceCftRecordResponsePayloadData] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
