# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/cflowd/applications/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, limit: Optional[int] = None, query: Optional[str] = None, **kw) -> Any:
        """
        Generate cflowd flows list in a grid table
        GET /dataservice/statistics/cflowd/applications/summary

        :param limit: Limit
        :param query: Query
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createFlowssummary")
        params = {
            "limit": limit,
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/cflowd/applications/summary", params=params, **kw
        )
