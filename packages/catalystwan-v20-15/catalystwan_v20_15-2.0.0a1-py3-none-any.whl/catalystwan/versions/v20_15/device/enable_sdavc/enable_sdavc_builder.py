# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class EnableSdavcBuilder:
    """
    Builds and executes requests for operations under /device/enableSDAVC
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, enable: bool, **kw):
        """
        Enable/Disable SDAVC on device
        POST /dataservice/device/enableSDAVC/{deviceIP}/{enable}

        :param device_ip: Device IP
        :param enable: Enable/Disable flag
        :returns: None
        """
        params = {
            "deviceIP": device_ip,
            "enable": enable,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/device/enableSDAVC/{deviceIP}/{enable}", params=params, **kw
        )
