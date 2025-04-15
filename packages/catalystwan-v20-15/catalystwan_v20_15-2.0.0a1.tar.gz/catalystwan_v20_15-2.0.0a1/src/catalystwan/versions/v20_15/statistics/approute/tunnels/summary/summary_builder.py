# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteTransportResp


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/tunnels/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: str,
        query: Optional[str] = None,
        limit: Optional[int] = 10,
        site_id: Optional[str] = None,
        **kw,
    ) -> AppRouteTransportResp:
        """
        Get tunnel top statistics from device
        GET /dataservice/statistics/approute/tunnels/summary/{type}

        :param type_: Type
        :param query: Query
        :param limit: Limit
        :param site_id: Site id
        :returns: AppRouteTransportResp
        """
        params = {
            "type": type_,
            "query": query,
            "limit": limit,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/tunnels/summary/{type}",
            return_type=AppRouteTransportResp,
            params=params,
            **kw,
        )
