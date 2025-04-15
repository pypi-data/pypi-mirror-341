# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DisablePacketCaptureRes


class DisableBuilder:
    """
    Builds and executes requests for operations under /stream/device/capture/disable
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: str, **kw) -> DisablePacketCaptureRes:
        """
        Disable packet capture session
        GET /dataservice/stream/device/capture/disable/{sessionId}

        :param session_id: Session id
        :returns: DisablePacketCaptureRes
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/capture/disable/{sessionId}",
            return_type=DisablePacketCaptureRes,
            params=params,
            **kw,
        )
