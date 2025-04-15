# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class RpMappingBuilder:
    """
    Builds and executes requests for operations under /device/pim/rp-mapping
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get PIM Rp-mapping list from device
        GET /dataservice/device/pim/rp-mapping

        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/pim/rp-mapping", return_type=List[Any], params=params, **kw
        )
