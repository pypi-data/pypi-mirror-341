# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TraceInfoResponsePayload


class TraceInfoByBaseKeyBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/traceInfoByBaseKey
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, entry_time: int, trace_model: Optional[str] = None, **kw
    ) -> TraceInfoResponsePayload:
        """
        Get TraceInfoByBaseKey
        GET /dataservice/stream/device/nwpi/traceInfoByBaseKey

        :param trace_id: traceId
        :param entry_time: entryTime
        :param trace_model: traceModel
        :returns: TraceInfoResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "getTraceInfoByBaseKey")
        params = {
            "traceId": trace_id,
            "entryTime": entry_time,
            "traceModel": trace_model,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/traceInfoByBaseKey",
            return_type=TraceInfoResponsePayload,
            params=params,
            **kw,
        )
