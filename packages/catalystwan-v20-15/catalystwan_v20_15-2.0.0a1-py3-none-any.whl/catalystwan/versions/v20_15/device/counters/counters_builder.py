# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceCountersResponse


class CountersBuilder:
    """
    Builds and executes requests for operations under /device/counters
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DeviceCountersResponse:
        """
        Get device counters
        GET /dataservice/device/counters

        :returns: DeviceCountersResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/counters", return_type=DeviceCountersResponse, **kw
        )
