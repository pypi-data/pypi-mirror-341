# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .capacity.capacity_builder import CapacityBuilder


class VsmartBuilder:
    """
    Builds and executes requests for operations under /tenant/vsmart
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Retrieve mapping of tenants to vSmarts


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenant/vsmart

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/tenant/vsmart", return_type=List[Any], **kw
        )

    def put(self, tenant_id: str, payload: Any, **kw) -> List[Any]:
        """
        Update placement of the Tenant from source vSmart to destination vSmart


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/tenant/{tenantId}/vsmart

        :param tenant_id: Tenant Id
        :param payload: Tenant model
        :returns: List[Any]
        """
        params = {
            "tenantId": tenant_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/tenant/{tenantId}/vsmart",
            return_type=List[Any],
            params=params,
            payload=payload,
            **kw,
        )

    @property
    def capacity(self) -> CapacityBuilder:
        """
        The capacity property
        """
        from .capacity.capacity_builder import CapacityBuilder

        return CapacityBuilder(self._request_adapter)
