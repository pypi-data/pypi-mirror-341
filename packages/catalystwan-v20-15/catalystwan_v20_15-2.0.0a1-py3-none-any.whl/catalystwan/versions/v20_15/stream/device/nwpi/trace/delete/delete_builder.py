# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiTraceDeleteRespPayload


class DeleteBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/trace/delete
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, trace_id: str, timestamp: int, **kw) -> NwpiTraceDeleteRespPayload:
        """
        Trace Action - Delete
        DELETE /dataservice/stream/device/nwpi/trace/delete

        :param trace_id: trace id
        :param timestamp: start time
        :returns: NwpiTraceDeleteRespPayload
        """
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/stream/device/nwpi/trace/delete",
            return_type=NwpiTraceDeleteRespPayload,
            params=params,
            **kw,
        )
