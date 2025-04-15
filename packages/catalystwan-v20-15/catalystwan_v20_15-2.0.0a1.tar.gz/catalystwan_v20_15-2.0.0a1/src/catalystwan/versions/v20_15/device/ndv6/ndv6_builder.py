# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import IfNameParam, VpnIdParam


class Ndv6Builder:
    """
    Builds and executes requests for operations under /device/ndv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        if_name: Optional[IfNameParam] = None,
        mac: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get IPv6 Neighbors from device (Real Time)
        GET /dataservice/device/ndv6

        :param vpn_id: VPN Id
        :param if_name: Interface name
        :param mac: Mac address
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "if-name": if_name,
            "mac": mac,
            "deviceId": device_id,
        }
        return self._request_adapter.request("GET", "/dataservice/device/ndv6", params=params, **kw)
