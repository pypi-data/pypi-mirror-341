# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SimpleMessageResponse


class StoptrackingBuilder:
    """
    Builds and executes requests for operations under /alarms/stoptracking
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, test_name: str, **kw) -> SimpleMessageResponse:
        """
        Stop tracking events
        POST /dataservice/alarms/stoptracking/{testName}

        :param test_name: Test Name
        :returns: SimpleMessageResponse
        """
        params = {
            "testName": test_name,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/alarms/stoptracking/{testName}",
            return_type=SimpleMessageResponse,
            params=params,
            **kw,
        )
