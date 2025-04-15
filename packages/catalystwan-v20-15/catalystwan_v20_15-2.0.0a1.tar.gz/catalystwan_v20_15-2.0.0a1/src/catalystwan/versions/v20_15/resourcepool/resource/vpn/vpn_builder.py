# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VpnBuilder:
    """
    Builds and executes requests for operations under /resourcepool/resource/vpn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, tenant_id: str, tenant_vpn: int, **kw) -> Any:
        """
        Get tenant device vpn resource
        GET /dataservice/resourcepool/resource/vpn

        :param tenant_id: Tenant Organization Name
        :param tenant_vpn: Tenant Vpn Number
        :returns: Any
        """
        params = {
            "tenantId": tenant_id,
            "tenantVpn": tenant_vpn,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/resourcepool/resource/vpn", params=params, **kw
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Create Vpn resource pool and return tenant device vpn
        PUT /dataservice/resourcepool/resource/vpn

        :param payload: create resources from resource pool
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/resourcepool/resource/vpn", payload=payload, **kw
        )

    def delete(self, tenant_id: str, tenant_vpn: int, **kw):
        """
        Delete tenant device vpn and release the resource
        DELETE /dataservice/resourcepool/resource/vpn

        :param tenant_id: Tenant Organization Name
        :param tenant_vpn: Tenant Vpn Number
        :returns: None
        """
        params = {
            "tenantId": tenant_id,
            "tenantVpn": tenant_vpn,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/resourcepool/resource/vpn", params=params, **kw
        )
