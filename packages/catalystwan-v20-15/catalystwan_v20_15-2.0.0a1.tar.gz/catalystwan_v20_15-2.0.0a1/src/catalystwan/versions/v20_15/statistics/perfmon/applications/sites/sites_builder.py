# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .health.health_builder import HealthBuilder


class SitesBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/applications/sites
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def health(self) -> HealthBuilder:
        """
        The health property
        """
        from .health.health_builder import HealthBuilder

        return HealthBuilder(self._request_adapter)
