# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /stream/device/log/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: str, **kw):
        """
        Get
        GET /dataservice/stream/device/log/download/{sessionId}

        :param session_id: Session Id
        :returns: None
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/stream/device/log/download/{sessionId}", params=params, **kw
        )
