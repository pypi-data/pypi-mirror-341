# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .port_speeds.port_speeds_builder import PortSpeedsBuilder


class ConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/connectivity/connections
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def port_speeds(self) -> PortSpeedsBuilder:
        """
        The port-speeds property
        """
        from .port_speeds.port_speeds_builder import PortSpeedsBuilder

        return PortSpeedsBuilder(self._request_adapter)
