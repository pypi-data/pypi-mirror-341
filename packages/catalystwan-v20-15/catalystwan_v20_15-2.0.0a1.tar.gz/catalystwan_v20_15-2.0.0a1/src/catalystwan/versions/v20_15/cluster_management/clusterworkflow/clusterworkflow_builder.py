# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .version.version_builder import VersionBuilder


class ClusterworkflowBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/clusterworkflow
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def version(self) -> VersionBuilder:
        """
        The version property
        """
        from .version.version_builder import VersionBuilder

        return VersionBuilder(self._request_adapter)
