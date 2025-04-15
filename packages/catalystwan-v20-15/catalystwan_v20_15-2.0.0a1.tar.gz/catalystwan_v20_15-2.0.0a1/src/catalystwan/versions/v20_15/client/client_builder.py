# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .server.server_builder import ServerBuilder
    from .token.token_builder import TokenBuilder


class ClientBuilder:
    """
    Builds and executes requests for operations under /client
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def server(self) -> ServerBuilder:
        """
        The server property
        """
        from .server.server_builder import ServerBuilder

        return ServerBuilder(self._request_adapter)

    @property
    def token(self) -> TokenBuilder:
        """
        The token property
        """
        from .token.token_builder import TokenBuilder

        return TokenBuilder(self._request_adapter)
