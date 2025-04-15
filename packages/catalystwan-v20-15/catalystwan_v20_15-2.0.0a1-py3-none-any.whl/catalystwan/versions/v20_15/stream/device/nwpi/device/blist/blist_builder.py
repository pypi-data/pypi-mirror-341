# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .del_.del_builder import DelBuilder
    from .get.get_builder import GetBuilder


class BlistBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/device/blist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def del_(self) -> DelBuilder:
        """
        The del property
        """
        from .del_.del_builder import DelBuilder

        return DelBuilder(self._request_adapter)

    @property
    def get(self) -> GetBuilder:
        """
        The get property
        """
        from .get.get_builder import GetBuilder

        return GetBuilder(self._request_adapter)
