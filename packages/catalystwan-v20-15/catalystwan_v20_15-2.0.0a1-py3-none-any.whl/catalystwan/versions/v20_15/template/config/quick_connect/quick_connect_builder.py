# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .submit_devices.submit_devices_builder import SubmitDevicesBuilder


class QuickConnectBuilder:
    """
    Builds and executes requests for operations under /template/config/quickConnect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def submit_devices(self) -> SubmitDevicesBuilder:
        """
        The submitDevices property
        """
        from .submit_devices.submit_devices_builder import SubmitDevicesBuilder

        return SubmitDevicesBuilder(self._request_adapter)
