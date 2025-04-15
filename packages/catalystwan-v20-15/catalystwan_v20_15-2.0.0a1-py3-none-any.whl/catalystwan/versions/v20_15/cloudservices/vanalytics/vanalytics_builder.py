# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dashboardlist.dashboardlist_builder import DashboardlistBuilder


class VanalyticsBuilder:
    """
    Builds and executes requests for operations under /cloudservices/vanalytics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def dashboardlist(self) -> DashboardlistBuilder:
        """
        The dashboardlist property
        """
        from .dashboardlist.dashboardlist_builder import DashboardlistBuilder

        return DashboardlistBuilder(self._request_adapter)
