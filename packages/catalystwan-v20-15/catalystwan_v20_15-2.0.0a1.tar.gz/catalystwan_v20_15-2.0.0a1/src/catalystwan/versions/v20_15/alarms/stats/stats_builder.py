# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmStatsResponse


class StatsBuilder:
    """
    Builds and executes requests for operations under /alarms/stats
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> AlarmStatsResponse:
        """
        Get alarm statistics
        GET /dataservice/alarms/stats

        :returns: AlarmStatsResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/stats", return_type=AlarmStatsResponse, **kw
        )
