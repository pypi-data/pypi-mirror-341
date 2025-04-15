# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QoSAggResp


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/qos/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: Optional[str] = None, **kw) -> List[QoSAggResp]:
        """
        Monitoring - QoS
        GET /dataservice/statistics/qos/aggregation

        :param query: Query
        :returns: List[QoSAggResp]
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/qos/aggregation",
            return_type=List[QoSAggResp],
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> List[QoSAggResp]:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/statistics/qos/aggregation

        :param payload: Stats query string
        :returns: List[QoSAggResp]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/qos/aggregation",
            return_type=List[QoSAggResp],
            payload=payload,
            **kw,
        )
