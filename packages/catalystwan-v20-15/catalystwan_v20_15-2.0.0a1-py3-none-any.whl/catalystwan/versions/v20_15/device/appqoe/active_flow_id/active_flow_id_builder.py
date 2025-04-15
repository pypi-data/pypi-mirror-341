# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ActiveFlowIdBuilder:
    """
    Builds and executes requests for operations under /device/appqoe/active-flow-id
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, flow_id: str, device_id: str, **kw) -> Any:
        """
        Get Appqoe Active flow Id details from device
        GET /dataservice/device/appqoe/active-flow-id

        :param flow_id: Flow Id
        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "flow-id": flow_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/appqoe/active-flow-id", params=params, **kw
        )
