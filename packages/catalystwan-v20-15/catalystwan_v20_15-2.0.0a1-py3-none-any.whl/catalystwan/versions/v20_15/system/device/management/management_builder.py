# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .systemip.systemip_builder import SystemipBuilder


class ManagementBuilder:
    """
    Builds and executes requests for operations under /system/device/management
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def systemip(self) -> SystemipBuilder:
        """
        The systemip property
        """
        from .systemip.systemip_builder import SystemipBuilder

        return SystemipBuilder(self._request_adapter)
