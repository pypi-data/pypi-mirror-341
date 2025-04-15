# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteAppAggRespInner


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/app-agg/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[AppRouteAppAggRespInner]:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/statistics/approute/app-agg/aggregation

        :param payload: Stats query string
        :returns: List[AppRouteAppAggRespInner]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/approute/app-agg/aggregation",
            return_type=List[AppRouteAppAggRespInner],
            payload=payload,
            **kw,
        )
