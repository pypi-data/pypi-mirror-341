# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .base.bases_builder import BasesBuilder
    from .compliance.compliance_builder import ComplianceBuilder
    from .default.default_builder import DefaultBuilder
    from .latest.latest_builder import LatestBuilder
    from .maintenance.maintenance_builder import MaintenanceBuilder


class ProtocolPackBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get all protocol packs details
        GET /dataservice/sdavc/protocol-pack

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/sdavc/protocol-pack", **kw)

    @property
    def bases_(self) -> BasesBuilder:
        """
        The bases_ property
        """
        from .base.bases_builder import BasesBuilder

        return BasesBuilder(self._request_adapter)

    @property
    def compliance(self) -> ComplianceBuilder:
        """
        The compliance property
        """
        from .compliance.compliance_builder import ComplianceBuilder

        return ComplianceBuilder(self._request_adapter)

    @property
    def default(self) -> DefaultBuilder:
        """
        The default property
        """
        from .default.default_builder import DefaultBuilder

        return DefaultBuilder(self._request_adapter)

    @property
    def latest(self) -> LatestBuilder:
        """
        The latest property
        """
        from .latest.latest_builder import LatestBuilder

        return LatestBuilder(self._request_adapter)

    @property
    def maintenance(self) -> MaintenanceBuilder:
        """
        The maintenance property
        """
        from .maintenance.maintenance_builder import MaintenanceBuilder

        return MaintenanceBuilder(self._request_adapter)
