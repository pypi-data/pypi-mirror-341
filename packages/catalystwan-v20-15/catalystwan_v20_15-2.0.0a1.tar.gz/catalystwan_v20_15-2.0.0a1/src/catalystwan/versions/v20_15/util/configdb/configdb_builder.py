# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .metrics.metrics_builder import MetricsBuilder
    from .size.size_builder import SizeBuilder


class ConfigdbBuilder:
    """
    Builds and executes requests for operations under /util/configdb
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def metrics(self) -> MetricsBuilder:
        """
        The metrics property
        """
        from .metrics.metrics_builder import MetricsBuilder

        return MetricsBuilder(self._request_adapter)

    @property
    def size(self) -> SizeBuilder:
        """
        The size property
        """
        from .size.size_builder import SizeBuilder

        return SizeBuilder(self._request_adapter)
