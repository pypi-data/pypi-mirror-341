# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class LatestBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/latest
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get current latest protocol pack details
        GET /dataservice/sdavc/protocol-pack/latest

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/sdavc/protocol-pack/latest", **kw)
