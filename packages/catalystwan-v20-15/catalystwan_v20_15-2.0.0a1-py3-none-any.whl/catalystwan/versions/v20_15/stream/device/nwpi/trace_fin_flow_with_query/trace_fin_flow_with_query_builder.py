# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpitraceFlowRespPayload


class TraceFinFlowWithQueryBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/traceFinFlowWithQuery
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, query: Optional[str] = None, **kw
    ) -> NwpitraceFlowRespPayload:
        """
        Retrieve Certain Fin Flows
        GET /dataservice/stream/device/nwpi/traceFinFlowWithQuery

        :param trace_id: trace id
        :param timestamp: start time
        :param query: Query filter
        :returns: NwpitraceFlowRespPayload
        """
        logging.warning("Operation: %s is deprecated", "traceFinFlowWithQuery")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/traceFinFlowWithQuery",
            return_type=NwpitraceFlowRespPayload,
            params=params,
            **kw,
        )
