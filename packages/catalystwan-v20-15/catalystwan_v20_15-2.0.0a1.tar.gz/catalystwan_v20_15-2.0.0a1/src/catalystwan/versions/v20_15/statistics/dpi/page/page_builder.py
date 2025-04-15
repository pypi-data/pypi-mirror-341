# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DpiPaginationResponse


class PageBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        **kw,
    ) -> DpiPaginationResponse:
        """
        Get DPI stats pagination raw data
        GET /dataservice/statistics/dpi/page

        :param query: Query
        :param scroll_id: Scroll id
        :param count: Count
        :returns: DpiPaginationResponse
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/dpi/page",
            return_type=DpiPaginationResponse,
            params=params,
            **kw,
        )

    def post(
        self, payload: Any, scroll_id: Optional[str] = None, count: Optional[int] = None, **kw
    ) -> DpiPaginationResponse:
        """
        Get DPI stats pagination raw data
        POST /dataservice/statistics/dpi/page

        :param scroll_id: Scroll id
        :param count: Count
        :param payload: User
        :returns: DpiPaginationResponse
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/dpi/page",
            return_type=DpiPaginationResponse,
            params=params,
            payload=payload,
            **kw,
        )
