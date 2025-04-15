# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .webex.webex_builder import WebexBuilder


class AppBuilder:
    """
    Builds and executes requests for operations under /cloudservices/app
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def webex(self) -> WebexBuilder:
        """
        The webex property
        """
        from .webex.webex_builder import WebexBuilder

        return WebexBuilder(self._request_adapter)
