# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ConnectResponse


class ConnectBuilder:
    """
    Builds and executes requests for operations under /ise/connect
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ConnectResponse:
        """
        Check if the configured ISE server is reachable
        GET /dataservice/ise/connect

        :returns: ConnectResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/ise/connect", return_type=ConnectResponse, **kw
        )
