# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class InfoBuilder:
    """
    Builds and executes requests for operations under /device/lacp/info
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, channel_group: Optional[str] = None, **kw) -> Any:
        """
        Get device lacp port channel info list (Real Time)
        GET /dataservice/device/lacp/info

        :param channel_group: Channel-group
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "channel-group": channel_group,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/lacp/info", params=params, **kw
        )
