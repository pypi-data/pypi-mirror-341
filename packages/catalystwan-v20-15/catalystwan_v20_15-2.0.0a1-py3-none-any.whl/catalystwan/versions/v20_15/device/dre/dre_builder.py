# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .auto_bypass_stats.auto_bypass_stats_builder import AutoBypassStatsBuilder
    from .dre_stats.dre_stats_builder import DreStatsBuilder
    from .dre_status.dre_status_builder import DreStatusBuilder
    from .peer_stats.peer_stats_builder import PeerStatsBuilder


class DreBuilder:
    """
    Builds and executes requests for operations under /device/dre
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def auto_bypass_stats(self) -> AutoBypassStatsBuilder:
        """
        The auto-bypass-stats property
        """
        from .auto_bypass_stats.auto_bypass_stats_builder import AutoBypassStatsBuilder

        return AutoBypassStatsBuilder(self._request_adapter)

    @property
    def dre_stats(self) -> DreStatsBuilder:
        """
        The dre-stats property
        """
        from .dre_stats.dre_stats_builder import DreStatsBuilder

        return DreStatsBuilder(self._request_adapter)

    @property
    def dre_status(self) -> DreStatusBuilder:
        """
        The dre-status property
        """
        from .dre_status.dre_status_builder import DreStatusBuilder

        return DreStatusBuilder(self._request_adapter)

    @property
    def peer_stats(self) -> PeerStatsBuilder:
        """
        The peer-stats property
        """
        from .peer_stats.peer_stats_builder import PeerStatsBuilder

        return PeerStatsBuilder(self._request_adapter)
