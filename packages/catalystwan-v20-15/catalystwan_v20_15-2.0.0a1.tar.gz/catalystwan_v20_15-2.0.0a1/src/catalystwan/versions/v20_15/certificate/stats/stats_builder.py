# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .detail.detail_builder import DetailBuilder
    from .summary.summary_builder import SummaryBuilder


class StatsBuilder:
    """
    Builds and executes requests for operations under /certificate/stats
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def detail(self) -> DetailBuilder:
        """
        The detail property
        """
        from .detail.detail_builder import DetailBuilder

        return DetailBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
