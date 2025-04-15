# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .log.log_builder import LogBuilder


class AppBuilder:
    """
    Builds and executes requests for operations under /device/app
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def log(self) -> LogBuilder:
        """
        The log property
        """
        from .log.log_builder import LogBuilder

        return LogBuilder(self._request_adapter)
