# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class InfoBuilder:
    """
    Builds and executes requests for operations under /server/info
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get Server info
        GET /dataservice/server/info

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/server/info", **kw)
