# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .partner_ports.partner_ports_builder import PartnerPortsBuilder


class ConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud/{cloud-type}/connectivity/connections
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def partner_ports(self) -> PartnerPortsBuilder:
        """
        The partner-ports property
        """
        from .partner_ports.partner_ports_builder import PartnerPortsBuilder

        return PartnerPortsBuilder(self._request_adapter)
