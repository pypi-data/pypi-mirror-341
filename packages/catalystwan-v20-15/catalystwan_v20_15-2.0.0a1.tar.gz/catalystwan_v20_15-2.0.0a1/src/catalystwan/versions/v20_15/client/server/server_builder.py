# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ClientServerInfoResponse


class ServerBuilder:
    """
    Builds and executes requests for operations under /client/server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ClientServerInfoResponse:
        """
        Get vManage server information
        GET /dataservice/client/server

        :returns: ClientServerInfoResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/client/server", return_type=ClientServerInfoResponse, **kw
        )
