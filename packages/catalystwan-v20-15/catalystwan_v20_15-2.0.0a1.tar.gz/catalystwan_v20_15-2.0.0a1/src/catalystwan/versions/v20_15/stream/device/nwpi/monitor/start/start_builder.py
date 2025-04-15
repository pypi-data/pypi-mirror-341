# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiMonitorReqPayload, NwpiMonitorRespPayload


class StartBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/monitor/start
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: NwpiMonitorReqPayload, **kw) -> NwpiMonitorRespPayload:
        """
        CXP Monitor Action - Start
        POST /dataservice/stream/device/nwpi/monitor/start

        :param payload: Payload
        :returns: NwpiMonitorRespPayload
        """
        logging.warning("Operation: %s is deprecated", "monitorStart")
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/monitor/start",
            return_type=NwpiMonitorRespPayload,
            payload=payload,
            **kw,
        )
