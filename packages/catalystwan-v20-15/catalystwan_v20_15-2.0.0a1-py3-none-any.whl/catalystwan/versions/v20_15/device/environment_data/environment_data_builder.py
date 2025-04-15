# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .radius_server.radius_server_builder import RadiusServerBuilder


class EnvironmentDataBuilder:
    """
    Builds and executes requests for operations under /device/environmentData
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        get Cisco TrustSec Environment Data information from device
        GET /dataservice/device/environmentData

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/environmentData", params=params, **kw
        )

    @property
    def radius_server(self) -> RadiusServerBuilder:
        """
        The radiusServer property
        """
        from .radius_server.radius_server_builder import RadiusServerBuilder

        return RadiusServerBuilder(self._request_adapter)
