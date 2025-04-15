# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .history.history_builder import HistoryBuilder
    from .overview.overview_builder import OverviewBuilder


class DevicehealthBuilder:
    """
    Builds and executes requests for operations under /statistics/devicehealth
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def history(self) -> HistoryBuilder:
        """
        The history property
        """
        from .history.history_builder import HistoryBuilder

        return HistoryBuilder(self._request_adapter)

    @property
    def overview(self) -> OverviewBuilder:
        """
        The overview property
        """
        from .overview.overview_builder import OverviewBuilder

        return OverviewBuilder(self._request_adapter)
