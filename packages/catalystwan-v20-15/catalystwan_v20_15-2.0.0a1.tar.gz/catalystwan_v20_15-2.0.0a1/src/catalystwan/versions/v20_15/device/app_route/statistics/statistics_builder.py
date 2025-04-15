# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LocalColorParam, RemoteColorParam


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /device/app-route/statistics
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        remote_system_ip: Optional[str] = None,
        local_color: Optional[LocalColorParam] = None,
        remote_color: Optional[RemoteColorParam] = None,
        **kw,
    ) -> Any:
        """
        Get application-aware routing statistics from device (Real Time)
        GET /dataservice/device/app-route/statistics

        :param remote_system_ip: Remote system IP
        :param local_color: Local color
        :param remote_color: Remote color
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "remote-system-ip": remote_system_ip,
            "local-color": local_color,
            "remote-color": remote_color,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/app-route/statistics", params=params, **kw
        )
