# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /dca/data/device/statistics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, stats_data_type: str, payload: Any, **kw) -> Any:
        """
        Get device statistics data
        POST /dataservice/dca/data/device/statistics/{stats_data_type}

        :param stats_data_type: Device statistics data
        :param payload: Query string
        :returns: Any
        """
        params = {
            "stats_data_type": stats_data_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/dca/data/device/statistics/{stats_data_type}",
            params=params,
            payload=payload,
            **kw,
        )
