# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class PageBuilder:
    """
    Builds and executes requests for operations under /statistics/bfd/page
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get stats raw data
        GET /dataservice/statistics/bfd/page

        :param query: Query string
        :param scroll_id: ES scroll Id
        :param count: Result size
        :returns: Any
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/bfd/page", params=params, **kw
        )

    def post(
        self, payload: Any, scroll_id: Optional[str] = None, count: Optional[int] = None, **kw
    ) -> Any:
        """
        Get stats raw data
        POST /dataservice/statistics/bfd/page

        :param scroll_id: ES scroll Id
        :param count: Result size
        :param payload: Stats query string
        :returns: Any
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/statistics/bfd/page", params=params, payload=payload, **kw
        )
