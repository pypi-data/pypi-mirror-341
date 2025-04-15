# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class UnreachableBuilder:
    """
    Builds and executes requests for operations under /device/unreachable
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, personality: str, **kw) -> List[Any]:
        """
        Get list of unreachable devices
        GET /dataservice/device/unreachable

        :param personality: Device personality (vedge OR vsmart OR vbond... )
        :returns: List[Any]
        """
        params = {
            "personality": personality,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/unreachable", return_type=List[Any], params=params, **kw
        )

    def delete(self, device_ip: str, **kw):
        """
        Delete unreachable device
        DELETE /dataservice/device/unreachable/{deviceIP}

        :param device_ip: Device IP
        :returns: None
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/unreachable/{deviceIP}", params=params, **kw
        )
