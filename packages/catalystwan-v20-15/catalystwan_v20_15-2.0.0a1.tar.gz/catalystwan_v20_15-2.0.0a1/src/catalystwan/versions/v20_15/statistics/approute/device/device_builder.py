# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .tunnel.tunnel_builder import TunnelBuilder
    from .tunnels.tunnels_builder import TunnelsBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def tunnel(self) -> TunnelBuilder:
        """
        The tunnel property
        """
        from .tunnel.tunnel_builder import TunnelBuilder

        return TunnelBuilder(self._request_adapter)

    @property
    def tunnels(self) -> TunnelsBuilder:
        """
        The tunnels property
        """
        from .tunnels.tunnels_builder import TunnelsBuilder

        return TunnelsBuilder(self._request_adapter)
