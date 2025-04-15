# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .networkinterface.networkinterface_builder import NetworkinterfaceBuilder
    from .networks.networks_builder import NetworksBuilder


class DefaultBuilder:
    """
    Builds and executes requests for operations under /template/feature/default
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def networkinterface(self) -> NetworkinterfaceBuilder:
        """
        The networkinterface property
        """
        from .networkinterface.networkinterface_builder import NetworkinterfaceBuilder

        return NetworkinterfaceBuilder(self._request_adapter)

    @property
    def networks(self) -> NetworksBuilder:
        """
        The networks property
        """
        from .networks.networks_builder import NetworksBuilder

        return NetworksBuilder(self._request_adapter)
