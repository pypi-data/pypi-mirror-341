# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PorthopcolorBuilder:
    """
    Builds and executes requests for operations under /device/tools/porthopcolor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, payload: Any, **kw):
        """
        Request port hop color
        POST /dataservice/device/tools/porthopcolor/{deviceIP}

        :param device_ip: Device IP
        :param payload: Device port hop color
        :returns: None
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/porthopcolor/{deviceIP}",
            params=params,
            payload=payload,
            **kw,
        )
