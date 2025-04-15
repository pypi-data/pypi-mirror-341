# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class GeneratePaygBuilder:
    """
    Builds and executes requests for operations under /system/device/generate-payg
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Authenticate vSmart user account
        POST /dataservice/system/device/generate-payg

        :param payload: Request body
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/system/device/generate-payg", payload=payload, **kw
        )
