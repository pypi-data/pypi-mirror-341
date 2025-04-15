# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnParam


class NslookupBuilder:
    """
    Builds and executes requests for operations under /device/tools/nslookup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vpn: VpnParam, dns: str, device_id: str, **kw) -> Any:
        """
        Get device tool nslookup
        GET /dataservice/device/tools/nslookup

        :param vpn: VPN
        :param dns: DNS
        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "vpn": vpn,
            "dns": dns,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/tools/nslookup", params=params, **kw
        )
