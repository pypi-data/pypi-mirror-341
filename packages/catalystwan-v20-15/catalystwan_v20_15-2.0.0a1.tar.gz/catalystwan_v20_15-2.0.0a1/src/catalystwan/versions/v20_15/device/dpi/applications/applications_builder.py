# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /device/dpi/applications
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        application: Optional[str] = None,
        family: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get DPI applications from device (Real Time)
        GET /dataservice/device/dpi/applications

        :param vpn_id: VPN Id
        :param application: Application
        :param family: Family
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "vpn-id": vpn_id,
            "application": application,
            "family": family,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/dpi/applications",
            return_type=List[Any],
            params=params,
            **kw,
        )
