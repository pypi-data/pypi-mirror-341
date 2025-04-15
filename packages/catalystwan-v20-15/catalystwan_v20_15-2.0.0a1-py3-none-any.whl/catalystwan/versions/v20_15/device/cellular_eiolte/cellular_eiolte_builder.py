# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connections.connections_builder import ConnectionsBuilder
    from .hardware.hardware_builder import HardwareBuilder
    from .ipsec.ipsec_builder import IpsecBuilder
    from .network.network_builder import NetworkBuilder
    from .radio.radio_builder import RadioBuilder
    from .sim.sim_builder import SimBuilder


class CellularEiolteBuilder:
    """
    Builds and executes requests for operations under /device/cellularEiolte
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connections(self) -> ConnectionsBuilder:
        """
        The connections property
        """
        from .connections.connections_builder import ConnectionsBuilder

        return ConnectionsBuilder(self._request_adapter)

    @property
    def hardware(self) -> HardwareBuilder:
        """
        The hardware property
        """
        from .hardware.hardware_builder import HardwareBuilder

        return HardwareBuilder(self._request_adapter)

    @property
    def ipsec(self) -> IpsecBuilder:
        """
        The ipsec property
        """
        from .ipsec.ipsec_builder import IpsecBuilder

        return IpsecBuilder(self._request_adapter)

    @property
    def network(self) -> NetworkBuilder:
        """
        The network property
        """
        from .network.network_builder import NetworkBuilder

        return NetworkBuilder(self._request_adapter)

    @property
    def radio(self) -> RadioBuilder:
        """
        The radio property
        """
        from .radio.radio_builder import RadioBuilder

        return RadioBuilder(self._request_adapter)

    @property
    def sim(self) -> SimBuilder:
        """
        The sim property
        """
        from .sim.sim_builder import SimBuilder

        return SimBuilder(self._request_adapter)
