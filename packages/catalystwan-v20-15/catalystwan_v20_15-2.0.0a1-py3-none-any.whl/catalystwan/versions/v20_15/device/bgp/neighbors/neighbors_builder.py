# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class NeighborsBuilder:
    """
    Builds and executes requests for operations under /device/bgp/neighbors
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        peer_addr: Optional[str] = None,
        as_: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get BGP neighbors list (Real Time)
        GET /dataservice/device/bgp/neighbors

        :param vpn_id: VPN Id
        :param peer_addr: Peer address
        :param as_: AS number
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "vpn-id": vpn_id,
            "peer-addr": peer_addr,
            "as": as_,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bgp/neighbors", return_type=List[Any], params=params, **kw
        )
