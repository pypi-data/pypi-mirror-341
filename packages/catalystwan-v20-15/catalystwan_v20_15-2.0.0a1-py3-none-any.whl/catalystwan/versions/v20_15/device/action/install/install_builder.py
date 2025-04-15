# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp

if TYPE_CHECKING:
    from .devices.devices_builder import DevicesBuilder


class InstallBuilder:
    """
    Builds and executes requests for operations under /device/action/install
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[DeviceIp], **kw):
        """
        Generate install info
        GET /dataservice/device/action/install

        :param device_id: deviceId - Device IP
        :returns: None
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/install", params=params, **kw
        )

    def post(self, payload: Any, **kw):
        """
        Process an installation operation
        POST /dataservice/device/action/install

        :param payload: Request body
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/install", payload=payload, **kw
        )

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
