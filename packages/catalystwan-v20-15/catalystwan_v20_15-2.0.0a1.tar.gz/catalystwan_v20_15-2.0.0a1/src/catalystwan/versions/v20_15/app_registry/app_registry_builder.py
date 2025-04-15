# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .app.app_builder import AppBuilder
    from .applications.applications_builder import ApplicationsBuilder
    from .clusters.clusters_builder import ClustersBuilder
    from .saasfeed.saasfeed_builder import SaasfeedBuilder


class AppRegistryBuilder:
    """
    Builds and executes requests for operations under /app-registry
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def app(self) -> AppBuilder:
        """
        The app property
        """
        from .app.app_builder import AppBuilder

        return AppBuilder(self._request_adapter)

    @property
    def applications(self) -> ApplicationsBuilder:
        """
        The applications property
        """
        from .applications.applications_builder import ApplicationsBuilder

        return ApplicationsBuilder(self._request_adapter)

    @property
    def clusters(self) -> ClustersBuilder:
        """
        The clusters property
        """
        from .clusters.clusters_builder import ClustersBuilder

        return ClustersBuilder(self._request_adapter)

    @property
    def saasfeed(self) -> SaasfeedBuilder:
        """
        The saasfeed property
        """
        from .saasfeed.saasfeed_builder import SaasfeedBuilder

        return SaasfeedBuilder(self._request_adapter)
