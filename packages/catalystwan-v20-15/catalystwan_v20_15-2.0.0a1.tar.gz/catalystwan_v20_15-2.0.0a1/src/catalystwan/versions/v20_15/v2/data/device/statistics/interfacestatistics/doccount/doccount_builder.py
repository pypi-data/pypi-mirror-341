# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DocCountRes


class DoccountBuilder:
    """
    Builds and executes requests for operations under /v2/data/device/statistics/interfacestatistics/doccount
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, start_date: str, end_date: str, time_zone: Optional[str] = None, **kw
    ) -> DocCountRes:
        """
        Get response count of a query
        GET /dataservice/v2/data/device/statistics/interfacestatistics/doccount

        :param start_date: Start date (example:2023-1-1T00:00:00)
        :param end_date: End date (example:2023-1-1T00:00:00)
        :param time_zone: Time zone (example:UTC)
        :returns: DocCountRes
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "timeZone": time_zone,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v2/data/device/statistics/interfacestatistics/doccount",
            return_type=DocCountRes,
            params=params,
            **kw,
        )
