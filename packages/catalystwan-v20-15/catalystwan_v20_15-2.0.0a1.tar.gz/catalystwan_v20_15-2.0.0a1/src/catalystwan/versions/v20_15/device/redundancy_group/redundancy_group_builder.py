# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .app_group.app_group_builder import AppGroupBuilder


class RedundancyGroupBuilder:
    """
    Builds and executes requests for operations under /device/redundancy-group
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def app_group(self) -> AppGroupBuilder:
        """
        The app-group property
        """
        from .app_group.app_group_builder import AppGroupBuilder

        return AppGroupBuilder(self._request_adapter)
