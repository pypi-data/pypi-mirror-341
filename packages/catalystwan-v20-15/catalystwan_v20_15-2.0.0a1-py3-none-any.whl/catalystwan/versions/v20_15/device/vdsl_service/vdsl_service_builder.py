# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .co_line_specific_stats.co_line_specific_stats_builder import CoLineSpecificStatsBuilder
    from .co_stats.co_stats_builder import CoStatsBuilder
    from .cpe_line_specific_stats.cpe_line_specific_stats_builder import CpeLineSpecificStatsBuilder
    from .cpe_stats.cpe_stats_builder import CpeStatsBuilder
    from .line_bonding_stats.line_bonding_stats_builder import LineBondingStatsBuilder
    from .line_specific_stats.line_specific_stats_builder import LineSpecificStatsBuilder
    from .vdsl_info.vdsl_info_builder import VdslInfoBuilder


class VdslServiceBuilder:
    """
    Builds and executes requests for operations under /device/vdslService
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def co_line_specific_stats(self) -> CoLineSpecificStatsBuilder:
        """
        The coLineSpecificStats property
        """
        from .co_line_specific_stats.co_line_specific_stats_builder import (
            CoLineSpecificStatsBuilder,
        )

        return CoLineSpecificStatsBuilder(self._request_adapter)

    @property
    def co_stats(self) -> CoStatsBuilder:
        """
        The coStats property
        """
        from .co_stats.co_stats_builder import CoStatsBuilder

        return CoStatsBuilder(self._request_adapter)

    @property
    def cpe_line_specific_stats(self) -> CpeLineSpecificStatsBuilder:
        """
        The cpeLineSpecificStats property
        """
        from .cpe_line_specific_stats.cpe_line_specific_stats_builder import (
            CpeLineSpecificStatsBuilder,
        )

        return CpeLineSpecificStatsBuilder(self._request_adapter)

    @property
    def cpe_stats(self) -> CpeStatsBuilder:
        """
        The cpeStats property
        """
        from .cpe_stats.cpe_stats_builder import CpeStatsBuilder

        return CpeStatsBuilder(self._request_adapter)

    @property
    def line_bonding_stats(self) -> LineBondingStatsBuilder:
        """
        The lineBondingStats property
        """
        from .line_bonding_stats.line_bonding_stats_builder import LineBondingStatsBuilder

        return LineBondingStatsBuilder(self._request_adapter)

    @property
    def line_specific_stats(self) -> LineSpecificStatsBuilder:
        """
        The lineSpecificStats property
        """
        from .line_specific_stats.line_specific_stats_builder import LineSpecificStatsBuilder

        return LineSpecificStatsBuilder(self._request_adapter)

    @property
    def vdsl_info(self) -> VdslInfoBuilder:
        """
        The vdslInfo property
        """
        from .vdsl_info.vdsl_info_builder import VdslInfoBuilder

        return VdslInfoBuilder(self._request_adapter)
