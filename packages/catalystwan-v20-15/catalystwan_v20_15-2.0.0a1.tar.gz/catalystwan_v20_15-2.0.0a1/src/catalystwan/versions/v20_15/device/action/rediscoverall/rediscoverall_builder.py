# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RediscoverallBuilder:
    """
    Builds and executes requests for operations under /device/action/rediscoverall
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw):
        """
        Rediscover all devices
        POST /dataservice/device/action/rediscoverall

        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/rediscoverall", **kw
        )
