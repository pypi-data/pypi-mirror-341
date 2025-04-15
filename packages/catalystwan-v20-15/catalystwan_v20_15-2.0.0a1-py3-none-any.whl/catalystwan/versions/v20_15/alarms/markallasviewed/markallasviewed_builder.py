# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class MarkallasviewedBuilder:
    """
    Builds and executes requests for operations under /alarms/markallasviewed
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, type_: Optional[str] = None, **kw):
        """
        Mark all alarms as acknowledged by the user
        POST /dataservice/alarms/markallasviewed

        :param type_: Specify type. Allowed values: ["active", "cleared"]
        :param payload: Query
        :returns: None
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/alarms/markallasviewed", params=params, payload=payload, **kw
        )
