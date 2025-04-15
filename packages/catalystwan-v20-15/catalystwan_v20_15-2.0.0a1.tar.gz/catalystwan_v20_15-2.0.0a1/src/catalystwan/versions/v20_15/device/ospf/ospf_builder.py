# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .database.database_builder import DatabaseBuilder
    from .databaseexternal.databaseexternal_builder import DatabaseexternalBuilder
    from .databasesummary.databasesummary_builder import DatabasesummaryBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .neighbor.neighbor_builder import NeighborBuilder
    from .process.process_builder import ProcessBuilder
    from .routes.routes_builder import RoutesBuilder
    from .v3interface.v3_interface_builder import V3InterfaceBuilder
    from .v3neighbor.v3_neighbor_builder import V3NeighborBuilder


class OspfBuilder:
    """
    Builds and executes requests for operations under /device/ospf
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def database(self) -> DatabaseBuilder:
        """
        The database property
        """
        from .database.database_builder import DatabaseBuilder

        return DatabaseBuilder(self._request_adapter)

    @property
    def databaseexternal(self) -> DatabaseexternalBuilder:
        """
        The databaseexternal property
        """
        from .databaseexternal.databaseexternal_builder import DatabaseexternalBuilder

        return DatabaseexternalBuilder(self._request_adapter)

    @property
    def databasesummary(self) -> DatabasesummaryBuilder:
        """
        The databasesummary property
        """
        from .databasesummary.databasesummary_builder import DatabasesummaryBuilder

        return DatabasesummaryBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def neighbor(self) -> NeighborBuilder:
        """
        The neighbor property
        """
        from .neighbor.neighbor_builder import NeighborBuilder

        return NeighborBuilder(self._request_adapter)

    @property
    def process(self) -> ProcessBuilder:
        """
        The process property
        """
        from .process.process_builder import ProcessBuilder

        return ProcessBuilder(self._request_adapter)

    @property
    def routes(self) -> RoutesBuilder:
        """
        The routes property
        """
        from .routes.routes_builder import RoutesBuilder

        return RoutesBuilder(self._request_adapter)

    @property
    def v3interface(self) -> V3InterfaceBuilder:
        """
        The v3interface property
        """
        from .v3interface.v3_interface_builder import V3InterfaceBuilder

        return V3InterfaceBuilder(self._request_adapter)

    @property
    def v3neighbor(self) -> V3NeighborBuilder:
        """
        The v3neighbor property
        """
        from .v3neighbor.v3_neighbor_builder import V3NeighborBuilder

        return V3NeighborBuilder(self._request_adapter)
