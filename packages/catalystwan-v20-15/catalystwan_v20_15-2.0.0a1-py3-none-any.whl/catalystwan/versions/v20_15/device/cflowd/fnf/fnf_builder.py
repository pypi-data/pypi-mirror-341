# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cache_stats.cache_stats_builder import CacheStatsBuilder
    from .export_client_stats.export_client_stats_builder import ExportClientStatsBuilder
    from .export_stats.export_stats_builder import ExportStatsBuilder
    from .flow_monitor.flow_monitor_builder import FlowMonitorBuilder
    from .monitor_stats.monitor_stats_builder import MonitorStatsBuilder


class FnfBuilder:
    """
    Builds and executes requests for operations under /device/cflowd/fnf
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cache_stats(self) -> CacheStatsBuilder:
        """
        The cache-stats property
        """
        from .cache_stats.cache_stats_builder import CacheStatsBuilder

        return CacheStatsBuilder(self._request_adapter)

    @property
    def export_client_stats(self) -> ExportClientStatsBuilder:
        """
        The export-client-stats property
        """
        from .export_client_stats.export_client_stats_builder import ExportClientStatsBuilder

        return ExportClientStatsBuilder(self._request_adapter)

    @property
    def export_stats(self) -> ExportStatsBuilder:
        """
        The export-stats property
        """
        from .export_stats.export_stats_builder import ExportStatsBuilder

        return ExportStatsBuilder(self._request_adapter)

    @property
    def flow_monitor(self) -> FlowMonitorBuilder:
        """
        The flow-monitor property
        """
        from .flow_monitor.flow_monitor_builder import FlowMonitorBuilder

        return FlowMonitorBuilder(self._request_adapter)

    @property
    def monitor_stats(self) -> MonitorStatsBuilder:
        """
        The monitor-stats property
        """
        from .monitor_stats.monitor_stats_builder import MonitorStatsBuilder

        return MonitorStatsBuilder(self._request_adapter)
