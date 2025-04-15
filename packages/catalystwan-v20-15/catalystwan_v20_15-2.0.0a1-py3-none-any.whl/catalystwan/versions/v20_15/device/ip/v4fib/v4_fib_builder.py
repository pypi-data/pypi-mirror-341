# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ColorParam, VpnIdParam


class V4FibBuilder:
    """
    Builds and executes requests for operations under /device/ip/v4fib
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        prefix: Optional[str] = None,
        tloc: Optional[str] = None,
        color: Optional[ColorParam] = None,
        **kw,
    ) -> Any:
        """
        Get IPv4 FIB list from device (Real Time)
        GET /dataservice/device/ip/v4fib

        :param vpn_id: VPN Id
        :param prefix: IP prefix
        :param tloc: tloc IP
        :param color: tloc color
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "prefix": prefix,
            "tloc": tloc,
            "color": color,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/ip/v4fib", params=params, **kw
        )
