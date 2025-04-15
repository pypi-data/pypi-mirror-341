# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiTraceStopRespPayload


class StopBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/trace/stop
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, trace_id: str, **kw) -> NwpiTraceStopRespPayload:
        """
        Trace Action - Stop
        POST /dataservice/stream/device/nwpi/trace/stop/{traceId}

        :param trace_id: traceId
        :returns: NwpiTraceStopRespPayload
        """
        params = {
            "traceId": trace_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/trace/stop/{traceId}",
            return_type=NwpiTraceStopRespPayload,
            params=params,
            **kw,
        )
