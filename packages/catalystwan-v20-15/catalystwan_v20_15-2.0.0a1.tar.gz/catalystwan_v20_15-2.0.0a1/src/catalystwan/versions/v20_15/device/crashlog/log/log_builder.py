# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class LogBuilder:
    """
    Builds and executes requests for operations under /device/crashlog/log
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, filename: str, **kw) -> str:
        """
        Get device crash info from device
        GET /dataservice/device/crashlog/log

        :param device_id: deviceId - Device IP
        :param filename: Crash file name
        :returns: str
        """
        params = {
            "deviceId": device_id,
            "filename": filename,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/crashlog/log", return_type=str, params=params, **kw
        )
