# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .vedges.vedges_builder import VedgesBuilder


class UnclaimedBuilder:
    """
    Builds and executes requests for operations under /device/unclaimed
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def vedges(self) -> VedgesBuilder:
        """
        The vedges property
        """
        from .vedges.vedges_builder import VedgesBuilder

        return VedgesBuilder(self._request_adapter)
