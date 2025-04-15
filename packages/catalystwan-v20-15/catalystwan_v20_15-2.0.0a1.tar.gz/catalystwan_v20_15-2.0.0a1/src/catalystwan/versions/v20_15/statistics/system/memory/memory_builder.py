# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MemoryBuilder:
    """
    Builds and executes requests for operations under /statistics/system/memory
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, device_id: str, **kw) -> Any:
        """
        Get device system memory stats list
        GET /dataservice/statistics/system/memory

        :param query: Query filter
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "query": query,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/system/memory", params=params, **kw
        )
