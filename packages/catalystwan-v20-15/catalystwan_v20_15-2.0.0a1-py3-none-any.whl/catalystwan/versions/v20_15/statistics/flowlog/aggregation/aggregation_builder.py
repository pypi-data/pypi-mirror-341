# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FlowlogAggregationResponse


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/flowlog/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: Optional[str] = None, **kw) -> FlowlogAggregationResponse:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        GET /dataservice/statistics/flowlog/aggregation

        :param query: Query
        :returns: FlowlogAggregationResponse
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/flowlog/aggregation",
            return_type=FlowlogAggregationResponse,
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> FlowlogAggregationResponse:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/statistics/flowlog/aggregation

        :param payload: Stats query string
        :returns: FlowlogAggregationResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/flowlog/aggregation",
            return_type=FlowlogAggregationResponse,
            payload=payload,
            **kw,
        )
