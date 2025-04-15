# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceComplianceSummaryResponse


class SummaryBuilder:
    """
    Builds and executes requests for operations under /device/compliance/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DeviceComplianceSummaryResponse:
        """
        Get compliance summary for devices
        GET /dataservice/device/compliance/summary

        :returns: DeviceComplianceSummaryResponse
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/compliance/summary",
            return_type=DeviceComplianceSummaryResponse,
            **kw,
        )
