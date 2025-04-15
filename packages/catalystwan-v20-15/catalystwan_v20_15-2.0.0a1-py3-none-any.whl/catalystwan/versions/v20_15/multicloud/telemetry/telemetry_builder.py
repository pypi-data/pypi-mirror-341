# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Taskid, TelemetryRequests


class TelemetryBuilder:
    """
    Builds and executes requests for operations under /multicloud/telemetry
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: TelemetryRequests, **kw) -> Taskid:
        """
        Reports telemetry data
        POST /dataservice/multicloud/telemetry

        :param payload: telemetry
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/telemetry", return_type=Taskid, payload=payload, **kw
        )
