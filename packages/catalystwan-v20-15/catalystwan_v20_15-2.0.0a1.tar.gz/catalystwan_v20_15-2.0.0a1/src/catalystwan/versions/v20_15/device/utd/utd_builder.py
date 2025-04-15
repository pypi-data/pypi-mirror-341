# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dataplane_config.dataplane_config_builder import DataplaneConfigBuilder
    from .dataplane_global.dataplane_global_builder import DataplaneGlobalBuilder
    from .dataplane_stats.dataplane_stats_builder import DataplaneStatsBuilder
    from .dataplane_stats_summary.dataplane_stats_summary_builder import (
        DataplaneStatsSummaryBuilder,
    )
    from .engine_instance_status.engine_instance_status_builder import EngineInstanceStatusBuilder
    from .engine_status.engine_status_builder import EngineStatusBuilder
    from .file_analysis_status.file_analysis_status_builder import FileAnalysisStatusBuilder
    from .file_reputation_status.file_reputation_status_builder import FileReputationStatusBuilder
    from .ips_update_status.ips_update_status_builder import IpsUpdateStatusBuilder
    from .signature.signature_builder import SignatureBuilder
    from .urlf_con_status.urlf_con_status_builder import UrlfConStatusBuilder
    from .urlf_update_status.urlf_update_status_builder import UrlfUpdateStatusBuilder
    from .version_status.version_status_builder import VersionStatusBuilder


class UtdBuilder:
    """
    Builds and executes requests for operations under /device/utd
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def dataplane_config(self) -> DataplaneConfigBuilder:
        """
        The dataplane-config property
        """
        from .dataplane_config.dataplane_config_builder import DataplaneConfigBuilder

        return DataplaneConfigBuilder(self._request_adapter)

    @property
    def dataplane_global(self) -> DataplaneGlobalBuilder:
        """
        The dataplane-global property
        """
        from .dataplane_global.dataplane_global_builder import DataplaneGlobalBuilder

        return DataplaneGlobalBuilder(self._request_adapter)

    @property
    def dataplane_stats(self) -> DataplaneStatsBuilder:
        """
        The dataplane-stats property
        """
        from .dataplane_stats.dataplane_stats_builder import DataplaneStatsBuilder

        return DataplaneStatsBuilder(self._request_adapter)

    @property
    def dataplane_stats_summary(self) -> DataplaneStatsSummaryBuilder:
        """
        The dataplane-stats-summary property
        """
        from .dataplane_stats_summary.dataplane_stats_summary_builder import (
            DataplaneStatsSummaryBuilder,
        )

        return DataplaneStatsSummaryBuilder(self._request_adapter)

    @property
    def engine_instance_status(self) -> EngineInstanceStatusBuilder:
        """
        The engine-instance-status property
        """
        from .engine_instance_status.engine_instance_status_builder import (
            EngineInstanceStatusBuilder,
        )

        return EngineInstanceStatusBuilder(self._request_adapter)

    @property
    def engine_status(self) -> EngineStatusBuilder:
        """
        The engine-status property
        """
        from .engine_status.engine_status_builder import EngineStatusBuilder

        return EngineStatusBuilder(self._request_adapter)

    @property
    def file_analysis_status(self) -> FileAnalysisStatusBuilder:
        """
        The file-analysis-status property
        """
        from .file_analysis_status.file_analysis_status_builder import FileAnalysisStatusBuilder

        return FileAnalysisStatusBuilder(self._request_adapter)

    @property
    def file_reputation_status(self) -> FileReputationStatusBuilder:
        """
        The file-reputation-status property
        """
        from .file_reputation_status.file_reputation_status_builder import (
            FileReputationStatusBuilder,
        )

        return FileReputationStatusBuilder(self._request_adapter)

    @property
    def ips_update_status(self) -> IpsUpdateStatusBuilder:
        """
        The ips-update-status property
        """
        from .ips_update_status.ips_update_status_builder import IpsUpdateStatusBuilder

        return IpsUpdateStatusBuilder(self._request_adapter)

    @property
    def signature(self) -> SignatureBuilder:
        """
        The signature property
        """
        from .signature.signature_builder import SignatureBuilder

        return SignatureBuilder(self._request_adapter)

    @property
    def urlf_con_status(self) -> UrlfConStatusBuilder:
        """
        The urlf-con-status property
        """
        from .urlf_con_status.urlf_con_status_builder import UrlfConStatusBuilder

        return UrlfConStatusBuilder(self._request_adapter)

    @property
    def urlf_update_status(self) -> UrlfUpdateStatusBuilder:
        """
        The urlf-update-status property
        """
        from .urlf_update_status.urlf_update_status_builder import UrlfUpdateStatusBuilder

        return UrlfUpdateStatusBuilder(self._request_adapter)

    @property
    def version_status(self) -> VersionStatusBuilder:
        """
        The version-status property
        """
        from .version_status.version_status_builder import VersionStatusBuilder

        return VersionStatusBuilder(self._request_adapter)
