# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ipv4.ipv4_builder import Ipv4Builder
    from .ipv6.ipv6_builder import Ipv6Builder


class Ospfv3Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def ipv4(self) -> Ipv4Builder:
        """
        The ipv4 property
        """
        from .ipv4.ipv4_builder import Ipv4Builder

        return Ipv4Builder(self._request_adapter)

    @property
    def ipv6(self) -> Ipv6Builder:
        """
        The ipv6 property
        """
        from .ipv6.ipv6_builder import Ipv6Builder

        return Ipv6Builder(self._request_adapter)
