# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceTypeParam, HealthParam, SiteHealthItem


class CommonBuilder:
    """
    Builds and executes requests for operations under /statistics/sitehealth/common
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        is_heat_map: Optional[str] = "false",
        last_n_hours: Optional[int] = None,
        interval: Optional[int] = 30,
        health: Optional[HealthParam] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        include_details: Optional[str] = "false",
        include_region: Optional[str] = "false",
        region_name: Optional[str] = None,
        device_type: Optional[DeviceTypeParam] = None,
        **kw,
    ) -> List[SiteHealthItem]:
        """
        Get all site health
        GET /dataservice/statistics/sitehealth/common

        :param is_heat_map: Is heat map
        :param last_n_hours: Last n hours
        :param interval: Interval
        :param health: Health
        :param start_time: Start time
        :param end_time: End time
        :param include_details: Include details
        :param include_region: Include region
        :param region_name: Region name
        :param device_type: Device type
        :returns: List[SiteHealthItem]
        """
        params = {
            "isHeatMap": is_heat_map,
            "last_n_hours": last_n_hours,
            "interval": interval,
            "health": health,
            "start_time": start_time,
            "end_time": end_time,
            "includeDetails": include_details,
            "includeRegion": include_region,
            "regionName": region_name,
            "deviceType": device_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/sitehealth/common",
            return_type=List[SiteHealthItem],
            params=params,
            **kw,
        )
