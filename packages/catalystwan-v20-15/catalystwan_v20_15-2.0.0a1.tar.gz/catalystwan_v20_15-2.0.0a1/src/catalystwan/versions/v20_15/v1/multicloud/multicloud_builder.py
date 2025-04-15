# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interconnect.interconnect_builder import InterconnectBuilder


class MulticloudBuilder:
    """
    Builds and executes requests for operations under /v1/multicloud
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def interconnect(self) -> InterconnectBuilder:
        """
        The interconnect property
        """
        from .interconnect.interconnect_builder import InterconnectBuilder

        return InterconnectBuilder(self._request_adapter)
