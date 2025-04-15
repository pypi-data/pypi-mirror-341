# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class StartmonitorBuilder:
    """
    Builds and executes requests for operations under /device/action/startmonitor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Triggers global monitoring thread
        GET /dataservice/device/action/startmonitor

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/device/action/startmonitor", **kw)
