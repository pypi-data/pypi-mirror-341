# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FlowlogPaginationResponse


class PageBuilder:
    """
    Builds and executes requests for operations under /statistics/flowlog/page
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
    ) -> FlowlogPaginationResponse:
        """
        Get stats pagination raw data
        GET /dataservice/statistics/flowlog/page

        :param query: Query string
        :param scroll_id: Scroll Id
        :param count: Result size
        :returns: FlowlogPaginationResponse
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/flowlog/page",
            return_type=FlowlogPaginationResponse,
            params=params,
            **kw,
        )

    def post(
        self, payload: Any, scroll_id: Optional[str] = None, count: Optional[int] = None, **kw
    ) -> FlowlogPaginationResponse:
        """
        Get stats pagination raw data
        POST /dataservice/statistics/flowlog/page

        :param scroll_id: Scroll Id
        :param count: Result size
        :param payload: Stats query string
        :returns: FlowlogPaginationResponse
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/flowlog/page",
            return_type=FlowlogPaginationResponse,
            params=params,
            payload=payload,
            **kw,
        )
