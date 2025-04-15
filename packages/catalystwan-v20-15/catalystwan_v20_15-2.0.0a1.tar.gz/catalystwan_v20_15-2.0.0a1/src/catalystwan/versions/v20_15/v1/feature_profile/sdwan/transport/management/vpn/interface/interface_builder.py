# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ethernet.ethernet_builder import EthernetBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/management/vpn/interface
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
