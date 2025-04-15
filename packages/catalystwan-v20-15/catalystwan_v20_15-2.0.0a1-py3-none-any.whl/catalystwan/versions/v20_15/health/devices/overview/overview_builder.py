# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class OverviewBuilder:
    """
    Builds and executes requests for operations under /health/devices/overview
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vpn_id: Optional[str] = None, **kw) -> Any:
        """
        gets devices health overview
        GET /dataservice/health/devices/overview

        :param vpn_id: Optional vpn ID to filter devices
        :returns: Any
        """
        params = {
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/health/devices/overview", params=params, **kw
        )
