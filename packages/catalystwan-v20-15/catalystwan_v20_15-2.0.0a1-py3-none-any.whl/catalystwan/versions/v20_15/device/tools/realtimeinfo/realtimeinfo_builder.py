# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RealtimeinfoBuilder:
    """
    Builds and executes requests for operations under /device/tools/realtimeinfo
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get hardware real time info from device
        GET /dataservice/device/tools/realtimeinfo

        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/tools/realtimeinfo", params=params, **kw
        )
