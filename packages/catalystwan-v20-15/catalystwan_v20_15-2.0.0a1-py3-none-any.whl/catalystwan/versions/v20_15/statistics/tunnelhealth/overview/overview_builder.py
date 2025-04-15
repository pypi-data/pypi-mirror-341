# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TunnelHealthOverview


class OverviewBuilder:
    """
    Builds and executes requests for operations under /statistics/tunnelhealth/overview
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: str,
        last_n_hours: Optional[int] = 12,
        site: Optional[str] = None,
        limit: Optional[int] = 30,
        **kw,
    ) -> TunnelHealthOverview:
        """
        Get all tunnel health overview
        GET /dataservice/statistics/tunnelhealth/overview/{type}

        :param type_: Type
        :param last_n_hours: Last n hours
        :param site: Site
        :param limit: Limit
        :returns: TunnelHealthOverview
        """
        params = {
            "type": type_,
            "last_n_hours": last_n_hours,
            "site": site,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/tunnelhealth/overview/{type}",
            return_type=TunnelHealthOverview,
            params=params,
            **kw,
        )
