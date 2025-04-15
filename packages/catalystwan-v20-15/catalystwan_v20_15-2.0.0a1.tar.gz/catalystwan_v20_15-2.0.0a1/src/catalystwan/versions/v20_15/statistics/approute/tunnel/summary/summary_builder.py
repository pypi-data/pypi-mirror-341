# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteRespWithPageInfo


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/tunnel/{type}/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: str, query: Optional[str] = None, **kw) -> List[AppRouteRespWithPageInfo]:
        """
        Get tunnel top statistics in as chart
        GET /dataservice/statistics/approute/tunnel/{type}/summary

        :param type_: Type
        :param query: Query
        :returns: List[AppRouteRespWithPageInfo]
        """
        params = {
            "type": type_,
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/tunnel/{type}/summary",
            return_type=List[AppRouteRespWithPageInfo],
            params=params,
            **kw,
        )
