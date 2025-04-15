# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppQosStateResponsePayloadInner


class AppQosStateBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/appQosState
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, trace_state: str, **kw
    ) -> List[AppQosStateResponsePayloadInner]:
        """
        Get QoS Application state to received timestamp mapping for NWPI.
        GET /dataservice/stream/device/nwpi/appQosState

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param trace_state: Trace state
        :returns: List[AppQosStateResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getAppQosState")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "traceState": trace_state,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/appQosState",
            return_type=List[AppQosStateResponsePayloadInner],
            params=params,
            **kw,
        )
