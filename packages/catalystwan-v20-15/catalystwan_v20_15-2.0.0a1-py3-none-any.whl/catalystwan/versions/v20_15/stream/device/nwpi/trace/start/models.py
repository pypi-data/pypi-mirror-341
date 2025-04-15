# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpiTraceStartRespPayloadTraces:
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    entry_time: Optional[int] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    message: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class NwpiTraceStartRespPayload:
    """
    Nwpi trace start response payload schema
    """

    action: Optional[str] = _field(default=None)
    domain_mon: Optional[bool] = _field(default=None, metadata={"alias": "domain-mon"})
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None, metadata={"alias": "expire-time"})
    local_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "local-drop-rate-threshold"}
    )
    qos_mon: Optional[bool] = _field(default=None, metadata={"alias": "qos-mon"})
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    state: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    traces: Optional[List[NwpiTraceStartRespPayloadTraces]] = _field(default=None)
    wan_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "wan-drop-rate-threshold"}
    )


@dataclass
class NwpiTraceStartReqPayload:
    """
    Trace start payload schema
    """

    app: Optional[List[str]] = _field(default=None)
    app_vis: Optional[str] = _field(default=None, metadata={"alias": "app-vis"})
    art_vis: Optional[str] = _field(default=None, metadata={"alias": "art-vis"})
    dia_vis: Optional[str] = _field(default=None, metadata={"alias": "dia-vis"})
    dscp: Optional[str] = _field(default=None)
    dst_pfx: Optional[str] = _field(default=None, metadata={"alias": "dst-pfx"})
    dst_port: Optional[str] = _field(default=None, metadata={"alias": "dst-port"})
    duration: Optional[str] = _field(default=None)
    hub_wan_vis: Optional[str] = _field(default=None, metadata={"alias": "hub-wan-vis"})
    protocol: Optional[str] = _field(default=None)
    sampling: Optional[str] = _field(default=None)
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    spl_intvl: Optional[str] = _field(default=None, metadata={"alias": "spl-intvl"})
    src_if: Optional[str] = _field(default=None, metadata={"alias": "src-if"})
    src_pfx: Optional[str] = _field(default=None, metadata={"alias": "src-pfx"})
    src_port: Optional[str] = _field(default=None, metadata={"alias": "src-port"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})
