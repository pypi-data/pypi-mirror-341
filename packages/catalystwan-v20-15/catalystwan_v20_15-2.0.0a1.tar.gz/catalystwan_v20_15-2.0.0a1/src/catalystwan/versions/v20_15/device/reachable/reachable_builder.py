# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceReachableData


class ReachableBuilder:
    """
    Builds and executes requests for operations under /device/reachable
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DeviceReachableData:
        """
        Get list of reachable devices
        GET /dataservice/device/reachable

        :returns: DeviceReachableData
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/reachable", return_type=DeviceReachableData, **kw
        )
