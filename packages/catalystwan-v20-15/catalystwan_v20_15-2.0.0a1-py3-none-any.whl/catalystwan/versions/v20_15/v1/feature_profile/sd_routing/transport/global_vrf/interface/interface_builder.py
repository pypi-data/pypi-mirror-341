# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ethernet.ethernet_builder import EthernetBuilder
    from .ipsec.ipsec_builder import IpsecBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface
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
    def ipsec(self) -> IpsecBuilder:
        """
        The ipsec property
        """
        from .ipsec.ipsec_builder import IpsecBuilder

        return IpsecBuilder(self._request_adapter)
