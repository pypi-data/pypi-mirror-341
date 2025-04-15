# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

EdgeType = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class InterconnectDashboardConnections:
    connectivity_name: Optional[str] = _field(default=None, metadata={"alias": "connectivityName"})
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})


@dataclass
class InterconnectDashboardLinkList:
    device_link_name: Optional[str] = _field(default=None, metadata={"alias": "deviceLinkName"})
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})


@dataclass
class InterconnectDashboard:
    connections: Optional[List[InterconnectDashboardConnections]] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    edge_account_id: Optional[str] = _field(default=None, metadata={"alias": "edgeAccountId"})
    edge_account_name: Optional[str] = _field(default=None, metadata={"alias": "edgeAccountName"})
    edge_gateway_id: Optional[str] = _field(default=None, metadata={"alias": "edgeGatewayId"})
    edge_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "edgeGatewayName"})
    edge_type: Optional[EdgeType] = _field(default=None, metadata={"alias": "edgeType"})
    link_list: Optional[List[InterconnectDashboardLinkList]] = _field(
        default=None, metadata={"alias": "linkList"}
    )
    region: Optional[str] = _field(default=None)
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})
    resource_state_update_ts: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateUpdateTs"}
    )
