# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TotalstatsBuilder:
    """
    Builds and executes requests for operations under /device/voicet1e1controllerinfo/totalstats
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Retrieve T1E1 controller total stats from device (Real Time)
        GET /dataservice/device/voicet1e1controllerinfo/totalstats

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/voicet1e1controllerinfo/totalstats", params=params, **kw
        )
