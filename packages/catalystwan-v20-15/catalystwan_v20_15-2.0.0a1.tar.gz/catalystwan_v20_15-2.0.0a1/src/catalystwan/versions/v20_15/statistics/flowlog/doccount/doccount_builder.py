# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CountResponse


class DoccountBuilder:
    """
    Builds and executes requests for operations under /statistics/flowlog/doccount
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> CountResponse:
        """
        Get response count of a query
        GET /dataservice/statistics/flowlog/doccount

        :param query: Query
        :returns: CountResponse
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/flowlog/doccount",
            return_type=CountResponse,
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> CountResponse:
        """
        Get response count of a query
        POST /dataservice/statistics/flowlog/doccount

        :param payload: Query
        :returns: CountResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/flowlog/doccount",
            return_type=CountResponse,
            payload=payload,
            **kw,
        )
