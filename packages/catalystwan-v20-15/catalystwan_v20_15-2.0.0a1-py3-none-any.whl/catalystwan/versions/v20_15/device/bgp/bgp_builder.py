# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .neighbors.neighbors_builder import NeighborsBuilder
    from .routes.routes_builder import RoutesBuilder
    from .summary.summary_builder import SummaryBuilder


class BgpBuilder:
    """
    Builds and executes requests for operations under /device/bgp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def neighbors(self) -> NeighborsBuilder:
        """
        The neighbors property
        """
        from .neighbors.neighbors_builder import NeighborsBuilder

        return NeighborsBuilder(self._request_adapter)

    @property
    def routes(self) -> RoutesBuilder:
        """
        The routes property
        """
        from .routes.routes_builder import RoutesBuilder

        return RoutesBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
