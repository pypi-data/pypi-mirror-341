# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpiDomainMonitorStateRespPayloadDevicelist:
    app_vis: Optional[str] = _field(default=None, metadata={"alias": "app-vis"})
    art_vis: Optional[str] = _field(default=None, metadata={"alias": "art-vis"})
    connected_v_manages: Optional[str] = _field(
        default=None, metadata={"alias": "connectedVManages"}
    )
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    dia_vis: Optional[str] = _field(default=None, metadata={"alias": "dia-vis"})
    domain_mon: Optional[str] = _field(default=None, metadata={"alias": "domain-mon"})
    domain_monitor_can_be_started: Optional[str] = _field(default=None)
    dscp_is_valid: Optional[str] = _field(default=None, metadata={"alias": "dscp-is-valid"})
    duration: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None, metadata={"alias": "expire-time"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    message: Optional[str] = _field(default=None)
    parent_trace_id: Optional[int] = _field(default=None, metadata={"alias": "parent-trace-id"})
    qos_mon: Optional[str] = _field(default=None, metadata={"alias": "qos-mon"})
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    state: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})


@dataclass
class NwpiTraceHistoryRespPayloadDataSummary:
    agg_client_prefix: Optional[str] = _field(default=None, metadata={"alias": "agg-client-prefix"})
    agg_src_sgt: Optional[str] = _field(default=None, metadata={"alias": "agg-src-sgt"})
    agg_svr_prefix: Optional[str] = _field(default=None, metadata={"alias": "agg-svr-prefix"})
    agg_user_name: Optional[str] = _field(default=None, metadata={"alias": "agg-user-name"})
    app: Optional[str] = _field(default=None)
    app_grp: Optional[str] = _field(default=None, metadata={"alias": "app-grp"})
    app_vis: Optional[str] = _field(default=None, metadata={"alias": "app-vis"})
    art_vis: Optional[str] = _field(default=None, metadata={"alias": "art-vis"})
    common_app: Optional[str] = _field(default=None)
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    devices_check_info: Optional[str] = _field(default=None, metadata={"alias": "devicesCheckInfo"})
    dia_vis: Optional[str] = _field(default=None, metadata={"alias": "dia-vis"})
    domain_mon: Optional[str] = _field(default=None, metadata={"alias": "domain-mon"})
    dscp: Optional[str] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None, metadata={"alias": "dst-ip"})
    dst_pfx: Optional[str] = _field(default=None, metadata={"alias": "dst-pfx"})
    dst_pfx_len: Optional[str] = _field(default=None, metadata={"alias": "dst-pfx-len"})
    dst_port: Optional[str] = _field(default=None, metadata={"alias": "dst-port"})
    duration: Optional[str] = _field(default=None)
    health_app_server_mem: Optional[str] = _field(
        default=None, metadata={"alias": "health-app-server-mem"}
    )
    health_cpu_core: Optional[str] = _field(default=None, metadata={"alias": "health-cpu-core"})
    health_cpu_load: Optional[str] = _field(default=None, metadata={"alias": "health-cpu-load"})
    health_cpu_load_average: Optional[str] = _field(
        default=None, metadata={"alias": "health-cpu-load-average"}
    )
    health_mem_usage: Optional[str] = _field(default=None, metadata={"alias": "health-mem-usage"})
    health_running_traces: Optional[int] = _field(
        default=None, metadata={"alias": "health-running-traces"}
    )
    health_server_ip: Optional[str] = _field(default=None, metadata={"alias": "health-server-ip"})
    hub_wan_vis: Optional[str] = _field(default=None, metadata={"alias": "hub-wan-vis"})
    local_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "local-drop-rate-threshold"}
    )
    message: Optional[str] = _field(default=None)
    protocol: Optional[str] = _field(default=None)
    qos_mon: Optional[str] = _field(default=None, metadata={"alias": "qos-mon"})
    sampling: Optional[str] = _field(default=None)
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    source_site_vmanage_version: Optional[str] = _field(
        default=None, metadata={"alias": "source-site-vmanage-version"}
    )
    spl_intvl: Optional[str] = _field(default=None, metadata={"alias": "spl-intvl"})
    src_if: Optional[str] = _field(default=None, metadata={"alias": "src-if"})
    src_ip: Optional[str] = _field(default=None, metadata={"alias": "src-ip"})
    src_pfx: Optional[str] = _field(default=None, metadata={"alias": "src-pfx"})
    src_pfx_len: Optional[str] = _field(default=None, metadata={"alias": "src-pfx-len"})
    src_port: Optional[str] = _field(default=None, metadata={"alias": "src-port"})
    state: Optional[str] = _field(default=None)
    stop_time: Optional[int] = _field(default=None, metadata={"alias": "stop-time"})
    task_id: Optional[int] = _field(default=None, metadata={"alias": "taskId"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    trace_stop_type: Optional[str] = _field(default=None)
    trace_trigger_event: Optional[str] = _field(
        default=None, metadata={"alias": "trace-trigger-event"}
    )
    username: Optional[str] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})
    vpn_list: Optional[str] = _field(default=None, metadata={"alias": "vpn-list"})
    wan_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "wan-drop-rate-threshold"}
    )
    warning: Optional[str] = _field(default=None)


@dataclass
class NwpiTraceHistoryRespPayloadData:
    devices: Optional[List[NwpiDomainMonitorStateRespPayloadDevicelist]] = _field(default=None)
    summary: Optional[NwpiTraceHistoryRespPayloadDataSummary] = _field(default=None)


@dataclass
class NwpiTraceHistoryRespPayload:
    """
    Nwpi traceHistory response payload schema
    """

    data: Optional[NwpiTraceHistoryRespPayloadData] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
