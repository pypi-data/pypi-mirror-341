# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Vpnid


class SummaryBuilder:
    """
    Builds and executes requests for operations under /device/bfd/sites/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vpn_id: List[Vpnid], is_cached: Optional[bool] = False, **kw) -> Any:
        """
        Get BFD site summary
        GET /dataservice/device/bfd/sites/summary

        :param is_cached: Flag for caching
        :param vpn_id: Filter VPN
        :returns: Any
        """
        params = {
            "isCached": is_cached,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/sites/summary", params=params, **kw
        )
