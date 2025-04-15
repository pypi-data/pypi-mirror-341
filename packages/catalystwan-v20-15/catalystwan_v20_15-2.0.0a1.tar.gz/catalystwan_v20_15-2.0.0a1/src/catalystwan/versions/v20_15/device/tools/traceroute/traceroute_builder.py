# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TracerouteRequest, TracerouteResponse


class TracerouteBuilder:
    """
    Builds and executes requests for operations under /device/tools/traceroute
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, payload: TracerouteRequest, **kw) -> TracerouteResponse:
        """
        Traceroute
        POST /dataservice/device/tools/traceroute/{deviceIP}

        :param device_ip: Device IP
        :param payload: Traceroute parameter
        :returns: TracerouteResponse
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/traceroute/{deviceIP}",
            return_type=TracerouteResponse,
            params=params,
            payload=payload,
            **kw,
        )
