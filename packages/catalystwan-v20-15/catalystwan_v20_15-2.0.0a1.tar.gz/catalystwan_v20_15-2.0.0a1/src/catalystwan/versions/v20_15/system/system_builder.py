# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder
    from .reverseproxy.reverseproxy_builder import ReverseproxyBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /system
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def reverseproxy(self) -> ReverseproxyBuilder:
        """
        The reverseproxy property
        """
        from .reverseproxy.reverseproxy_builder import ReverseproxyBuilder

        return ReverseproxyBuilder(self._request_adapter)
