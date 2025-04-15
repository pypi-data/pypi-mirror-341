# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ClearBuilder:
    """
    Builds and executes requests for operations under /alarms/clear
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Clear the alarm for a specific UUID.
        POST /dataservice/alarms/clear

        :param payload: Clear Alarm
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/alarms/clear", payload=payload, **kw
        )
