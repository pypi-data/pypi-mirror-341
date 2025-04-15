# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DoccountBuilder:
    """
    Builds and executes requests for operations under /statistics/art/doccount
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> Any:
        """
        Get response count of a query
        GET /dataservice/statistics/art/doccount

        :param query: Query
        :returns: Any
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/art/doccount", params=params, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Get response count of a query
        POST /dataservice/statistics/art/doccount

        :param payload: Query
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/statistics/art/doccount", payload=payload, **kw
        )
