# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MwBuilder:
    """
    Builds and executes requests for operations under /device/action/status/mw
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get status of maintenance window for vManage upgrade flag
        GET /dataservice/device/action/status/mw

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/action/status/mw", **kw)

    def post(self, payload: Any, **kw):
        """
        Update maintenance window flag
        POST /dataservice/device/action/status/mw

        :param payload: Update maintenance window flag
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/status/mw", payload=payload, **kw
        )
