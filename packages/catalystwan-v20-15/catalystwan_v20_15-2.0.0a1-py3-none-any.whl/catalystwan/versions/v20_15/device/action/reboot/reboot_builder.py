# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp, TaskId

if TYPE_CHECKING:
    from .devices.devices_builder import DevicesBuilder


class RebootBuilder:
    """
    Builds and executes requests for operations under /device/action/reboot
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[DeviceIp], **kw) -> List[Any]:
        """
        Get device reboot information
        GET /dataservice/device/action/reboot

        :param device_id: Device Id
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/reboot", return_type=List[Any], params=params, **kw
        )

    def post(self, payload: Any, **kw) -> TaskId:
        """
        Process a reboot operation
        POST /dataservice/device/action/reboot

        :param payload: Device reboot request payload
        :returns: TaskId
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/reboot", return_type=TaskId, payload=payload, **kw
        )

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
