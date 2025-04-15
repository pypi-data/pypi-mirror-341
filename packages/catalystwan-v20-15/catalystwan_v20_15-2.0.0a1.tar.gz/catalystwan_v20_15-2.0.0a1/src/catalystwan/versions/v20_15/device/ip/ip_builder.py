# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .fib.fib_builder import FibBuilder
    from .ip_routes.ip_routes_builder import IpRoutesBuilder
    from .mfiboil.mfiboil_builder import MfiboilBuilder
    from .mfibstats.mfibstats_builder import MfibstatsBuilder
    from .mfibsummary.mfibsummary_builder import MfibsummaryBuilder
    from .nat64.nat64_builder import Nat64Builder
    from .nat.nat_builder import NatBuilder
    from .routetable.routetable_builder import RoutetableBuilder
    from .v4fib.v4_fib_builder import V4FibBuilder
    from .v6fib.v6_fib_builder import V6FibBuilder


class IpBuilder:
    """
    Builds and executes requests for operations under /device/ip
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def fib(self) -> FibBuilder:
        """
        The fib property
        """
        from .fib.fib_builder import FibBuilder

        return FibBuilder(self._request_adapter)

    @property
    def ip_routes(self) -> IpRoutesBuilder:
        """
        The ipRoutes property
        """
        from .ip_routes.ip_routes_builder import IpRoutesBuilder

        return IpRoutesBuilder(self._request_adapter)

    @property
    def mfiboil(self) -> MfiboilBuilder:
        """
        The mfiboil property
        """
        from .mfiboil.mfiboil_builder import MfiboilBuilder

        return MfiboilBuilder(self._request_adapter)

    @property
    def mfibstats(self) -> MfibstatsBuilder:
        """
        The mfibstats property
        """
        from .mfibstats.mfibstats_builder import MfibstatsBuilder

        return MfibstatsBuilder(self._request_adapter)

    @property
    def mfibsummary(self) -> MfibsummaryBuilder:
        """
        The mfibsummary property
        """
        from .mfibsummary.mfibsummary_builder import MfibsummaryBuilder

        return MfibsummaryBuilder(self._request_adapter)

    @property
    def nat(self) -> NatBuilder:
        """
        The nat property
        """
        from .nat.nat_builder import NatBuilder

        return NatBuilder(self._request_adapter)

    @property
    def nat64(self) -> Nat64Builder:
        """
        The nat64 property
        """
        from .nat64.nat64_builder import Nat64Builder

        return Nat64Builder(self._request_adapter)

    @property
    def routetable(self) -> RoutetableBuilder:
        """
        The routetable property
        """
        from .routetable.routetable_builder import RoutetableBuilder

        return RoutetableBuilder(self._request_adapter)

    @property
    def v4fib(self) -> V4FibBuilder:
        """
        The v4fib property
        """
        from .v4fib.v4_fib_builder import V4FibBuilder

        return V4FibBuilder(self._request_adapter)

    @property
    def v6fib(self) -> V6FibBuilder:
        """
        The v6fib property
        """
        from .v6fib.v6_fib_builder import V6FibBuilder

        return V6FibBuilder(self._request_adapter)
