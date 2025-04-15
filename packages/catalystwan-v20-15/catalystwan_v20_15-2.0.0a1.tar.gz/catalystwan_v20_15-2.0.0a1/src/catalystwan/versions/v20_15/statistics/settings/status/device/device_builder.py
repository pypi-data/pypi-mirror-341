# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DeviceBuilder:
    """
    Builds and executes requests for operations under /statistics/settings/status/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get list of enabled device for statistics index
        GET /dataservice/statistics/settings/status/device

        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/settings/status/device", params=params, **kw
        )
