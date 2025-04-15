# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class EventsBuilder:
    """
    Builds and executes requests for operations under /admin/events
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, sse_session_id: str, **kw):
        """
        Get
        GET /dataservice/admin/events/{sseSessionId}

        :param sse_session_id: sse session Id
        :returns: None
        """
        params = {
            "sseSessionId": sse_session_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/admin/events/{sseSessionId}", params=params, **kw
        )
