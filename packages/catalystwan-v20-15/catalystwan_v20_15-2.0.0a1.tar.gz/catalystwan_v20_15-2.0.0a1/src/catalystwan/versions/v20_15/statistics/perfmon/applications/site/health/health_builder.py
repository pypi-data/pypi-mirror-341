# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationsSiteItem, HealthParam, LastNHoursParam


class HealthBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/applications/site/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        siteid: str,
        is_heat_map: Optional[bool] = None,
        last_n_hours: Optional[LastNHoursParam] = None,
        health: Optional[HealthParam] = None,
        include_usage: Optional[bool] = False,
        **kw,
    ) -> List[ApplicationsSiteItem]:
        """
        Get all applications health for one site
        GET /dataservice/statistics/perfmon/applications/site/health

        :param siteid: Siteid
        :param is_heat_map: Is heat map
        :param last_n_hours: Last n hours
        :param health: Health
        :param include_usage: Include usage
        :returns: List[ApplicationsSiteItem]
        """
        params = {
            "siteid": siteid,
            "isHeatMap": is_heat_map,
            "last_n_hours": last_n_hours,
            "health": health,
            "includeUsage": include_usage,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/perfmon/applications/site/health",
            return_type=List[ApplicationsSiteItem],
            params=params,
            **kw,
        )
