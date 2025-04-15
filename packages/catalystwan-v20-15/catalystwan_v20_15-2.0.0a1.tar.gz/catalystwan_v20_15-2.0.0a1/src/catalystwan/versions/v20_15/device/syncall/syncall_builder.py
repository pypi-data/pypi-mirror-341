# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .memorydb.memorydb_builder import MemorydbBuilder


class SyncallBuilder:
    """
    Builds and executes requests for operations under /device/syncall
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def memorydb(self) -> MemorydbBuilder:
        """
        The memorydb property
        """
        from .memorydb.memorydb_builder import MemorydbBuilder

        return MemorydbBuilder(self._request_adapter)
