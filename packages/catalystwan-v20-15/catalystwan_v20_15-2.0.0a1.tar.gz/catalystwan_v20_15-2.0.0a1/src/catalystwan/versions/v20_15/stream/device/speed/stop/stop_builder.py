# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SpeedTestStatusResponse, Uuid


class StopBuilder:
    """
    Builds and executes requests for operations under /stream/device/speed/stop
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: Uuid, **kw) -> SpeedTestStatusResponse:
        """
        Get
        GET /dataservice/stream/device/speed/stop/{sessionId}

        :param session_id: sessionId
        :returns: SpeedTestStatusResponse
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/speed/stop/{sessionId}",
            return_type=SpeedTestStatusResponse,
            params=params,
            **kw,
        )
