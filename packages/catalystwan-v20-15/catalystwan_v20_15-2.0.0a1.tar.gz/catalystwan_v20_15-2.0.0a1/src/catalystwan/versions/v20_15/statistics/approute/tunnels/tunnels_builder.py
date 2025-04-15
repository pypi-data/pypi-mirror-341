# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteRespWithPageInfo

if TYPE_CHECKING:
    from .health.health_builder import HealthBuilder
    from .summary.summary_builder import SummaryBuilder


class TunnelsBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/tunnels
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, type_: str, query: Optional[str] = None, limit: Optional[int] = None, **kw
    ) -> List[AppRouteRespWithPageInfo]:
        """
        Get tunnel top statistics from device
        GET /dataservice/statistics/approute/tunnels/{type}

        :param type_: Type
        :param query: Query filter
        :param limit: Limit
        :returns: List[AppRouteRespWithPageInfo]
        """
        params = {
            "type": type_,
            "query": query,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/tunnels/{type}",
            return_type=List[AppRouteRespWithPageInfo],
            params=params,
            **kw,
        )

    @property
    def health(self) -> HealthBuilder:
        """
        The health property
        """
        from .health.health_builder import HealthBuilder

        return HealthBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
