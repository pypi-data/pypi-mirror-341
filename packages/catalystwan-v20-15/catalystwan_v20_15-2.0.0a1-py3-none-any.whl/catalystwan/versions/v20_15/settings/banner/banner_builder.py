# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class BannerBuilder:
    """
    Builds and executes requests for operations under /settings/banner
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve banner
        GET /dataservice/settings/banner

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/settings/banner", **kw)
