# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class AccesstokenBuilder:
    """
    Builds and executes requests for operations under /cloudservices/accesstoken
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get
        GET /dataservice/cloudservices/accesstoken

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/cloudservices/accesstoken", **kw)
