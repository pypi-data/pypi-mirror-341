# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sslproxy.sslproxy_builder import SslproxyBuilder


class CsrBuilder:
    """
    Builds and executes requests for operations under /sslproxy/generate/csr
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sslproxy(self) -> SslproxyBuilder:
        """
        The sslproxy property
        """
        from .sslproxy.sslproxy_builder import SslproxyBuilder

        return SslproxyBuilder(self._request_adapter)
