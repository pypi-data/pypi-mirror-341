# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connection.connection_builder import ConnectionBuilder


class TransportBuilder:
    """
    Builds and executes requests for operations under /device/transport
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connection(self) -> ConnectionBuilder:
        """
        The connection property
        """
        from .connection.connection_builder import ConnectionBuilder

        return ConnectionBuilder(self._request_adapter)
