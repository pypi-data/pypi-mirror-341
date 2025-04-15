# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FecAndPktDupResponse


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/recovery/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> FecAndPktDupResponse:
        """
        Get aggregation data and fec recovery rate if available
        POST /dataservice/statistics/dpi/recovery/aggregation

        :param payload: User
        :returns: FecAndPktDupResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/dpi/recovery/aggregation",
            return_type=FecAndPktDupResponse,
            payload=payload,
            **kw,
        )
