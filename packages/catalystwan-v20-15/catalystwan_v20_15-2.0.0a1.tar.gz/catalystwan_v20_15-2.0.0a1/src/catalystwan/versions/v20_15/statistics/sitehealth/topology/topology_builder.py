# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SiteHealthTopologyItem


class TopologyBuilder:
    """
    Builds and executes requests for operations under /statistics/sitehealth/topology
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        last_n_hours: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        interval: Optional[int] = 30,
        **kw,
    ) -> List[SiteHealthTopologyItem]:
        """
        Get all site health topology
        GET /dataservice/statistics/sitehealth/topology

        :param last_n_hours: Last n hours
        :param start_time: Start time
        :param end_time: End time
        :param interval: Interval
        :returns: List[SiteHealthTopologyItem]
        """
        params = {
            "last_n_hours": last_n_hours,
            "start_time": start_time,
            "end_time": end_time,
            "interval": interval,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/sitehealth/topology",
            return_type=List[SiteHealthTopologyItem],
            params=params,
            **kw,
        )
