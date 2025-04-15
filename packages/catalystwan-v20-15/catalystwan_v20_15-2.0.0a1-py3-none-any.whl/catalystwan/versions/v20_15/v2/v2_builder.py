# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .data.data_builder import DataBuilder


class V2Builder:
    """
    Builds and executes requests for operations under /v2
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def data(self) -> DataBuilder:
        """
        The data property
        """
        from .data.data_builder import DataBuilder

        return DataBuilder(self._request_adapter)
