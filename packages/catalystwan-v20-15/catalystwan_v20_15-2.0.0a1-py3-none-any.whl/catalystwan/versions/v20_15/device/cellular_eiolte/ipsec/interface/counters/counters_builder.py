# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CountersBuilder:
    """
    Builds and executes requests for operations under /device/cellularEiolte/ipsec/interface/counters
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get cellular ipsec interface info from device
        GET /dataservice/device/cellularEiolte/ipsec/interface/counters

        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/cellularEiolte/ipsec/interface/counters",
            params=params,
            **kw,
        )
