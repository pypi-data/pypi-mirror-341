# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateDeviceList


class DevicesBuilder:
    """
    Builds and executes requests for operations under /device/action/install/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_type: str, group_id: Optional[str] = None, **kw) -> GenerateDeviceList:
        """
        Get list of installed devices
        GET /dataservice/device/action/install/devices/{deviceType}

        :param device_type: Device type
        :param group_id: groupId
        :returns: GenerateDeviceList
        """
        params = {
            "deviceType": device_type,
            "groupId": group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/install/devices/{deviceType}",
            return_type=GenerateDeviceList,
            params=params,
            **kw,
        )
