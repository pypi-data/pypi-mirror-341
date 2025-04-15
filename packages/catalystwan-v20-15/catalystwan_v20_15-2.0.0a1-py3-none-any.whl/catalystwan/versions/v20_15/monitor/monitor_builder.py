# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sdavccloudconnector.sdavccloudconnector_builder import SdavccloudconnectorBuilder


class MonitorBuilder:
    """
    Builds and executes requests for operations under /monitor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sdavccloudconnector(self) -> SdavccloudconnectorBuilder:
        """
        The sdavccloudconnector property
        """
        from .sdavccloudconnector.sdavccloudconnector_builder import SdavccloudconnectorBuilder

        return SdavccloudconnectorBuilder(self._request_adapter)
