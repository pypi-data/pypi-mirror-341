# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class LicensedDeviceCountBuilder:
    """
    Builds and executes requests for operations under /msla/monitoring/licensedDeviceCount
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get licenses associated to device
        GET /dataservice/msla/monitoring/licensedDeviceCount

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/msla/monitoring/licensedDeviceCount", **kw
        )
