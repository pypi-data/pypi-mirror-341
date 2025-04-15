# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceStatusData


class DevicestatusBuilder:
    """
    Builds and executes requests for operations under /device/devicestatus
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DeviceStatusData:
        """
        Get devices status per type
        GET /dataservice/device/devicestatus

        :returns: DeviceStatusData
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/devicestatus", return_type=DeviceStatusData, **kw
        )
