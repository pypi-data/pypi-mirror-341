# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiDomainMonitorStateRespPayload


class GetMonitorStateBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/getMonitorState
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, trace_id: int, state: str, **kw) -> NwpiDomainMonitorStateRespPayload:
        """
        getMonitorState
        GET /dataservice/stream/device/nwpi/getMonitorState

        :param trace_id: trace id
        :param state: trace state
        :returns: NwpiDomainMonitorStateRespPayload
        """
        logging.warning("Operation: %s is deprecated", "getMonitorState")
        params = {
            "traceId": trace_id,
            "state": state,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/getMonitorState",
            return_type=NwpiDomainMonitorStateRespPayload,
            params=params,
            **kw,
        )
