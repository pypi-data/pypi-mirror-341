# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventReadoutFilterResponsePayload


class TraceReadoutFilterBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/traceReadoutFilter
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: List[int], entry_time: List[int], **kw
    ) -> EventReadoutFilterResponsePayload:
        """
        Get event Readout Filter By Traces
        GET /dataservice/stream/device/nwpi/traceReadoutFilter

        :param trace_id: traceId
        :param entry_time: entry_time
        :returns: EventReadoutFilterResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "getTraceReadoutFilter")
        params = {
            "trace_id": trace_id,
            "entry_time": entry_time,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/traceReadoutFilter",
            return_type=EventReadoutFilterResponsePayload,
            params=params,
            **kw,
        )
