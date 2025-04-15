# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .rebootcount.rebootcount_builder import RebootcountBuilder
    from .summary.summary_builder import SummaryBuilder


class IssuesBuilder:
    """
    Builds and executes requests for operations under /network/issues
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def rebootcount(self) -> RebootcountBuilder:
        """
        The rebootcount property
        """
        from .rebootcount.rebootcount_builder import RebootcountBuilder

        return RebootcountBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
