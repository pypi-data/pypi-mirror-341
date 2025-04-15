# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ethernet.ethernet_builder import EthernetBuilder
    from .gre.gre_builder import GreBuilder
    from .ipsec.ipsec_builder import IpsecBuilder
    from .svi.svi_builder import SviBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn/interface
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def ethernet(self) -> EthernetBuilder:
        """
        The ethernet property
        """
        from .ethernet.ethernet_builder import EthernetBuilder

        return EthernetBuilder(self._request_adapter)

    @property
    def gre(self) -> GreBuilder:
        """
        The gre property
        """
        from .gre.gre_builder import GreBuilder

        return GreBuilder(self._request_adapter)

    @property
    def ipsec(self) -> IpsecBuilder:
        """
        The ipsec property
        """
        from .ipsec.ipsec_builder import IpsecBuilder

        return IpsecBuilder(self._request_adapter)

    @property
    def svi(self) -> SviBuilder:
        """
        The svi property
        """
        from .svi.svi_builder import SviBuilder

        return SviBuilder(self._request_adapter)
