# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .async_.async_builder import AsyncBuilder


class BulkBuilder:
    """
    Builds and executes requests for operations under /tenant/bulk
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def async_(self) -> AsyncBuilder:
        """
        The async property
        """
        from .async_.async_builder import AsyncBuilder

        return AsyncBuilder(self._request_adapter)
