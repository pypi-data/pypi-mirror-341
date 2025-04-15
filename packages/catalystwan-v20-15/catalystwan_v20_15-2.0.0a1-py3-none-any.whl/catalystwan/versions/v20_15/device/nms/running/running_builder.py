# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class RunningBuilder:
    """
    Builds and executes requests for operations under /device/nms/running
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get nms running state from device
        GET /dataservice/device/nms/running

        :param device_id: Device Id
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/nms/running", return_type=List[Any], params=params, **kw
        )
