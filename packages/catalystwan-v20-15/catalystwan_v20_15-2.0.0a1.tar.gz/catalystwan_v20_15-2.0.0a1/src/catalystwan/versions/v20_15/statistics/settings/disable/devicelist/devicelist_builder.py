# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DevicelistBuilder:
    """
    Builds and executes requests for operations under /statistics/settings/disable/devicelist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, index_name: str, **kw) -> Any:
        """
        Get list of disabled devices for a statistics index
        GET /dataservice/statistics/settings/disable/devicelist/{indexName}

        :param index_name: Index name
        :returns: Any
        """
        params = {
            "indexName": index_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/settings/disable/devicelist/{indexName}",
            params=params,
            **kw,
        )

    def put(self, index_name: str, payload: Any, **kw) -> Any:
        """
        Update list of disabled devices for a statistics index
        PUT /dataservice/statistics/settings/disable/devicelist/{indexName}

        :param index_name: Index name
        :param payload: Disabled device
        :returns: Any
        """
        params = {
            "indexName": index_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/statistics/settings/disable/devicelist/{indexName}",
            params=params,
            payload=payload,
            **kw,
        )
