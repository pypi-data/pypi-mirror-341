# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .stats.stats_builder import StatsBuilder


class UcseBuilder:
    """
    Builds and executes requests for operations under /device/ucse
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def stats(self) -> StatsBuilder:
        """
        The stats property
        """
        from .stats.stats_builder import StatsBuilder

        return StatsBuilder(self._request_adapter)
