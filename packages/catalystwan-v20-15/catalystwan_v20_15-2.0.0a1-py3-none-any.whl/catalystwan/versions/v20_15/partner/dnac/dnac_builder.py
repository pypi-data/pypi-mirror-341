# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sda.sda_builder import SdaBuilder


class DnacBuilder:
    """
    Builds and executes requests for operations under /partner/dnac
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sda(self) -> SdaBuilder:
        """
        The sda property
        """
        from .sda.sda_builder import SdaBuilder

        return SdaBuilder(self._request_adapter)
