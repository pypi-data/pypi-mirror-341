# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class TunnelsInner:
    """
    CGW details relevant to AWS/AWS_GOVCLOUD
    """

    accepted_route_count: Optional[int] = _field(
        default=None, metadata={"alias": "acceptedRouteCount"}
    )
    last_status_change_timestamp: Optional[str] = _field(
        default=None, metadata={"alias": "lastStatusChangeTimestamp"}
    )
    outer_ip_addr: Optional[str] = _field(default=None, metadata={"alias": "outerIpAddr"})
    status: Optional[str] = _field(default=None)
    status_message: Optional[str] = _field(default=None, metadata={"alias": "statusMessage"})
    tunnel_id: Optional[str] = _field(default=None, metadata={"alias": "tunnelId"})
    tunnel_inner_ip: Optional[List[str]] = _field(default=None, metadata={"alias": "tunnelInnerIp"})


@dataclass
class GetSitesResponse:
    accelerated_vpn: Optional[bool] = _field(default=None, metadata={"alias": "acceleratedVpn"})
    agg_tunnel_status: Optional[str] = _field(default=None, metadata={"alias": "aggTunnelStatus"})
    attached: Optional[bool] = _field(default=None)
    color: Optional[str] = _field(default=None)
    hostname: Optional[str] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    preferred_interface: Optional[bool] = _field(
        default=None, metadata={"alias": "preferredInterface"}
    )
    private_ip: Optional[str] = _field(default=None, metadata={"alias": "privateIp"})
    public_ip: Optional[str] = _field(default=None, metadata={"alias": "publicIp"})
    site_id: Optional[str] = _field(default=None, metadata={"alias": "siteId"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "systemIp"})
    tunnel_count: Optional[int] = _field(default=None, metadata={"alias": "tunnelCount"})
    # CGW details relevant to AWS/AWS_GOVCLOUD
    tunnels: Optional[List[TunnelsInner]] = _field(default=None)
    uuid: Optional[str] = _field(default=None)


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)


@dataclass
class TunnelScalingRequestPayloadBranchEndpoints:
    accelerated_vpn: str = _field(metadata={"alias": "acceleratedVpn"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    color: str
    site_id: str = _field(metadata={"alias": "siteId"})
    system_ip: str = _field(metadata={"alias": "systemIp"})
    tunnel_count: str = _field(metadata={"alias": "tunnelCount"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "hostName"})
    interface: Optional[str] = _field(default=None)
    preferred_interface: Optional[str] = _field(
        default=None, metadata={"alias": "preferredInterface"}
    )
    public_ip: Optional[str] = _field(default=None, metadata={"alias": "publicIp"})
    solution: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    uuid: Optional[str] = _field(default=None)


@dataclass
class TunnelScalingRequestPayload:
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    branch_endpoints: Optional[List[TunnelScalingRequestPayloadBranchEndpoints]] = _field(
        default=None, metadata={"alias": "branchEndpoints"}
    )


@dataclass
class AttachSitesRequestPayloadInner:
    color: str
    site_id: str = _field(metadata={"alias": "siteId"})
    # Multicloud Branch Connect Solution type
    solution: str
    system_ip: str = _field(metadata={"alias": "systemIp"})
    tunnel_count: str = _field(metadata={"alias": "tunnelCount"})
    accelerated_vpn: Optional[str] = _field(default=None, metadata={"alias": "acceleratedVpn"})
    interface: Optional[str] = _field(default=None)
    preferred_interface: Optional[str] = _field(
        default=None, metadata={"alias": "preferredInterface"}
    )
    public_ip: Optional[str] = _field(default=None, metadata={"alias": "publicIp"})


@dataclass
class DetachSitesRequestPayloadInner:
    site_id: str = _field(metadata={"alias": "siteId"})
    system_ip: str = _field(metadata={"alias": "systemIp"})
    color: Optional[str] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    solution: Optional[str] = _field(default=None)
