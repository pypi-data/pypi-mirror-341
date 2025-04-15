# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceTlocDataWithBfd


class TlocBuilder:
    """
    Builds and executes requests for operations under /device/tloc
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, device_id: Optional[str] = None, color: Optional[str] = None, **kw
    ) -> DeviceTlocDataWithBfd:
        """
        Get TLOC status list
        GET /dataservice/device/tloc

        :param device_id: Device id
        :param color: Color
        :returns: DeviceTlocDataWithBfd
        """
        params = {
            "deviceId": device_id,
            "color": color,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/tloc",
            return_type=DeviceTlocDataWithBfd,
            params=params,
            **kw,
        )
