# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .bgp.bgp_builder import BgpBuilder
    from .ospf.ospf_builder import OspfBuilder
    from .ospfv3.ospfv3_builder import Ospfv3Builder


class RoutingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/routing
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def bgp(self) -> BgpBuilder:
        """
        The bgp property
        """
        from .bgp.bgp_builder import BgpBuilder

        return BgpBuilder(self._request_adapter)

    @property
    def ospf(self) -> OspfBuilder:
        """
        The ospf property
        """
        from .ospf.ospf_builder import OspfBuilder

        return OspfBuilder(self._request_adapter)

    @property
    def ospfv3(self) -> Ospfv3Builder:
        """
        The ospfv3 property
        """
        from .ospfv3.ospfv3_builder import Ospfv3Builder

        return Ospfv3Builder(self._request_adapter)
