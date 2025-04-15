# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteTunnenSummarResp


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/device/tunnel/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: Optional[str] = None, **kw) -> List[AppRouteTunnenSummarResp]:
        """
        Get statistics for top applications per tunnel in a grid table
        GET /dataservice/statistics/approute/device/tunnel/summary

        :param query: Query filter
        :returns: List[AppRouteTunnenSummarResp]
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/device/tunnel/summary",
            return_type=List[AppRouteTunnenSummarResp],
            params=params,
            **kw,
        )
