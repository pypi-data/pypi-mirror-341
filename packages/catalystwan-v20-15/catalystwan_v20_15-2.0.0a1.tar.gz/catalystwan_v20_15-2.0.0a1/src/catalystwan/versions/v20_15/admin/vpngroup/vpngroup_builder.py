# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class VpngroupBuilder:
    """
    Builds and executes requests for operations under /admin/vpngroup
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get VPN groups
        GET /dataservice/admin/vpngroup

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/admin/vpngroup", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw):
        """
        Add VPN group
        POST /dataservice/admin/vpngroup

        :param payload: VPN group
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/vpngroup", payload=payload, **kw
        )

    def put(self, id: str, payload: Any, **kw):
        """
        Update VPN group
        PUT /dataservice/admin/vpngroup/{id}

        :param id: VPN group Id
        :param payload: VPN group
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/admin/vpngroup/{id}", params=params, payload=payload, **kw
        )

    def delete(self, id: str, **kw):
        """
        Delete VPN group
        DELETE /dataservice/admin/vpngroup/{id}

        :param id: VPN group Id
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/admin/vpngroup/{id}", params=params, **kw
        )
