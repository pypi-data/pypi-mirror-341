# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .webserver.webserver_builder import WebserverBuilder


class ConfigurationBuilder:
    """
    Builds and executes requests for operations under /setting/configuration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def webserver(self) -> WebserverBuilder:
        """
        The webserver property
        """
        from .webserver.webserver_builder import WebserverBuilder

        return WebserverBuilder(self._request_adapter)
