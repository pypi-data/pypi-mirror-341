# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class AccesstokenBuilder:
    """
    Builds and executes requests for operations under /accesstoken
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, client_id: str, region_base_uri: str, **kw) -> str:
        """
        Get Access Token for SecureX Ribbon
        GET /dataservice/accesstoken/{regionBaseUri}/{clientId}

        :param client_id: Client id
        :param region_base_uri: Region base uri
        :returns: str
        """
        params = {
            "clientId": client_id,
            "regionBaseUri": region_base_uri,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/accesstoken/{regionBaseUri}/{clientId}",
            return_type=str,
            params=params,
            **kw,
        )
