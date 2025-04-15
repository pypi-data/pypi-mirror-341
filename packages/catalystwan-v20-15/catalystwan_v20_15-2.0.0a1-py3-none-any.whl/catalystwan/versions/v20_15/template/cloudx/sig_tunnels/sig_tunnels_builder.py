# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class SigTunnelsBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/sig_tunnels
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw):
        """
        Get Secure Internet Gateway Tunnel List
        GET /dataservice/template/cloudx/sig_tunnels

        :param device_id: DeviceIp/SystemIp
        :returns: None
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/sig_tunnels", params=params, **kw
        )
