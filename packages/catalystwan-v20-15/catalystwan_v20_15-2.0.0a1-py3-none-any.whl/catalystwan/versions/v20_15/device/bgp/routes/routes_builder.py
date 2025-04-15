# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class RoutesBuilder:
    """
    Builds and executes requests for operations under /device/bgp/routes
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        prefix: Optional[str] = None,
        nexthop: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get BGP routes list (Real Time)
        GET /dataservice/device/bgp/routes

        :param vpn_id: VPN Id
        :param prefix: IP prefix
        :param nexthop: Next hop
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "vpn-id": vpn_id,
            "prefix": prefix,
            "nexthop": nexthop,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bgp/routes", return_type=List[Any], params=params, **kw
        )
