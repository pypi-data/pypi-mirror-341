# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp/saas/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_ip: str, **kw):
        """
        Get Cloud On Ramp App details per device
        GET /dataservice/v1/cloudonramp/saas/status

        :param device_ip: DeviceIp/SystemIp
        :returns: None
        """
        params = {
            "deviceIp": device_ip,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/v1/cloudonramp/saas/status", params=params, **kw
        )
