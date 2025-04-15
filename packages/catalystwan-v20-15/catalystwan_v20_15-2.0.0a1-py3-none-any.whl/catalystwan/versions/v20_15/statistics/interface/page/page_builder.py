# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterfaceAggRespWithPageInfo


class PageBuilder:
    """
    Builds and executes requests for operations under /statistics/interface/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, query: str, count: str, scroll_id: Optional[str] = None, **kw
    ) -> InterfaceAggRespWithPageInfo:
        """
        Get stats raw data
        GET /dataservice/statistics/interface/page

        :param query: Query
        :param scroll_id: Scroll id
        :param count: Count
        :returns: InterfaceAggRespWithPageInfo
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/interface/page",
            return_type=InterfaceAggRespWithPageInfo,
            params=params,
            **kw,
        )

    def post(
        self, count: str, payload: Any, scroll_id: Optional[str] = None, **kw
    ) -> InterfaceAggRespWithPageInfo:
        """
        Get stats raw data
        POST /dataservice/statistics/interface/page

        :param scroll_id: Scroll id
        :param count: Count
        :param payload: Query filter
        :returns: InterfaceAggRespWithPageInfo
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/interface/page",
            return_type=InterfaceAggRespWithPageInfo,
            params=params,
            payload=payload,
            **kw,
        )
