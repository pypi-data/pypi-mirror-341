# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .mobility.mobility_builder import MobilityBuilder
    from .nfvirtual.nfvirtual_builder import NfvirtualBuilder
    from .sd_routing.sd_routing_builder import SdRoutingBuilder
    from .sdwan.sdwan_builder import SdwanBuilder


class FeatureProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def mobility(self) -> MobilityBuilder:
        """
        The mobility property
        """
        from .mobility.mobility_builder import MobilityBuilder

        return MobilityBuilder(self._request_adapter)

    @property
    def nfvirtual(self) -> NfvirtualBuilder:
        """
        The nfvirtual property
        """
        from .nfvirtual.nfvirtual_builder import NfvirtualBuilder

        return NfvirtualBuilder(self._request_adapter)

    @property
    def sd_routing(self) -> SdRoutingBuilder:
        """
        The sd-routing property
        """
        from .sd_routing.sd_routing_builder import SdRoutingBuilder

        return SdRoutingBuilder(self._request_adapter)

    @property
    def sdwan(self) -> SdwanBuilder:
        """
        The sdwan property
        """
        from .sdwan.sdwan_builder import SdwanBuilder

        return SdwanBuilder(self._request_adapter)
