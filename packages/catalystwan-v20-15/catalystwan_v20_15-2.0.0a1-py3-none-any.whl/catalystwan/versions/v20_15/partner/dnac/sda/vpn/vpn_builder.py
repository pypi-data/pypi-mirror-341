# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnListRes


class VpnBuilder:
    """
    Builds and executes requests for operations under /partner/dnac/sda/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> VpnListRes:
        """
        Get Overlay VPN list
        GET /dataservice/partner/dnac/sda/vpn

        :returns: VpnListRes
        """
        return self._request_adapter.request(
            "GET", "/dataservice/partner/dnac/sda/vpn", return_type=VpnListRes, **kw
        )
