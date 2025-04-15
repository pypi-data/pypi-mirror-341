# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class WidgetStatusStatusList:
    count: Optional[int] = _field(default=None)
    message: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)


@dataclass
class AllOfcloudWidgetCgwDeviceStatus:
    count: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[WidgetStatusStatusList]] = _field(
        default=None, metadata={"alias": "statusList"}
    )
    unreachable_count: Optional[int] = _field(default=None, metadata={"alias": "unreachableCount"})


@dataclass
class WidgetStatus:
    count: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[WidgetStatusStatusList]] = _field(
        default=None, metadata={"alias": "statusList"}
    )


@dataclass
class CloudWidget:
    cgw_device_site_ids: Optional[List[str]] = _field(
        default=None, metadata={"alias": "cgwDeviceSiteIds"}
    )
    cgw_device_status: Optional[AllOfcloudWidgetCgwDeviceStatus] = _field(
        default=None, metadata={"alias": "cgwDeviceStatus"}
    )
    cgw_sites_status: Optional[WidgetStatus] = _field(
        default=None, metadata={"alias": "cgwSitesStatus"}
    )
    cgw_status: Optional[WidgetStatus] = _field(default=None, metadata={"alias": "cgwStatus"})
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    num_accounts: Optional[int] = _field(default=None, metadata={"alias": "numAccounts"})
    num_tags: Optional[int] = _field(default=None, metadata={"alias": "numTags"})
    num_tunnels: Optional[int] = _field(default=None, metadata={"alias": "numTunnels"})
    num_vpcs: Optional[int] = _field(default=None, metadata={"alias": "numVpcs"})
    num_vpns: Optional[int] = _field(default=None, metadata={"alias": "numVpns"})
