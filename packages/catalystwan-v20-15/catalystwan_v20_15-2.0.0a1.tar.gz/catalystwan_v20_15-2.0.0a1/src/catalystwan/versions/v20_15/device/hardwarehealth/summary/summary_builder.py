# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /device/hardwarehealth/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vpn_id: List[str], is_cached: Optional[bool] = False, **kw) -> List[Any]:
        """
        Get hardware health summary for device
        GET /dataservice/device/hardwarehealth/summary

        :param is_cached: Status cached
        :param vpn_id: VPN Id
        :returns: List[Any]
        """
        params = {
            "isCached": is_cached,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/hardwarehealth/summary",
            return_type=List[Any],
            params=params,
            **kw,
        )
