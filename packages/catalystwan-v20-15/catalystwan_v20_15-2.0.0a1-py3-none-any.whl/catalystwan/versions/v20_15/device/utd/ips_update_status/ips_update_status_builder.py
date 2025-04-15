# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IpsUpdateStatusBuilder:
    """
    Builds and executes requests for operations under /device/utd/ips-update-status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get UTD IPS update status from device (Real Time)
        GET /dataservice/device/utd/ips-update-status

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/utd/ips-update-status", params=params, **kw
        )
