# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sla_class.sla_class_builder import SlaClassBuilder
    from .statistics.statistics_builder import StatisticsBuilder


class AppRouteBuilder:
    """
    Builds and executes requests for operations under /device/app-route
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sla_class(self) -> SlaClassBuilder:
        """
        The sla-class property
        """
        from .sla_class.sla_class_builder import SlaClassBuilder

        return SlaClassBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)
