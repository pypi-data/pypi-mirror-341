# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ExportTraceBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/exportTrace
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, trace_id: int, timestamp: int, **kw) -> Any:
        """
        Export NWPI Trace Data
        GET /dataservice/stream/device/nwpi/exportTrace

        :param trace_id: trace id
        :param timestamp: start time
        :returns: Any
        """
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/stream/device/nwpi/exportTrace", params=params, **kw
        )
