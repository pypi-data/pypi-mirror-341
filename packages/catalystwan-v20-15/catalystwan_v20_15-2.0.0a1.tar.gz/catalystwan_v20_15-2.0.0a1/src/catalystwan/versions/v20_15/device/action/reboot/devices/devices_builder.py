# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateRebootDeviceList


class DevicesBuilder:
    """
    Builds and executes requests for operations under /device/action/reboot/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_type: str, group_id: str, **kw) -> GenerateRebootDeviceList:
        """
        Get list of rebooted devices
        GET /dataservice/device/action/reboot/devices/{deviceType}

        :param device_type: Device type
        :param group_id: groupId
        :returns: GenerateRebootDeviceList
        """
        params = {
            "deviceType": device_type,
            "groupId": group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/reboot/devices/{deviceType}",
            return_type=GenerateRebootDeviceList,
            params=params,
            **kw,
        )
