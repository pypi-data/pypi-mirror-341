# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import StatisticsDbQueryParam


class CellularAggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/eiolte/cellularAggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: StatisticsDbQueryParam, **kw) -> Any:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/statistics/eiolte/cellularAggregation

        :param payload: Stats query string
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/statistics/eiolte/cellularAggregation", payload=payload, **kw
        )
