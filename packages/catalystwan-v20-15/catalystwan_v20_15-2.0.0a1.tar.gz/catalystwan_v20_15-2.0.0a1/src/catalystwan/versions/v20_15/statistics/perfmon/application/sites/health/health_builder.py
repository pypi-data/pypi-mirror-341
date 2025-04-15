# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationSitesItem, HealthParam, LastNHoursParam


class HealthBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/application/sites/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        application: str,
        is_heat_map: Optional[bool] = None,
        last_n_hours: Optional[LastNHoursParam] = None,
        health: Optional[HealthParam] = None,
        **kw,
    ) -> List[ApplicationSitesItem]:
        """
        Get one application health for all sites
        GET /dataservice/statistics/perfmon/application/sites/health

        :param application: Application
        :param is_heat_map: Is heat map
        :param last_n_hours: Last n hours
        :param health: Health
        :returns: List[ApplicationSitesItem]
        """
        params = {
            "application": application,
            "isHeatMap": is_heat_map,
            "last_n_hours": last_n_hours,
            "health": health,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/perfmon/application/sites/health",
            return_type=List[ApplicationSitesItem],
            params=params,
            **kw,
        )
