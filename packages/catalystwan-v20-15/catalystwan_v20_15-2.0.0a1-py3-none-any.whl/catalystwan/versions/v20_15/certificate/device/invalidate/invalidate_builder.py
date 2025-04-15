# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class InvalidateBuilder:
    """
    Builds and executes requests for operations under /certificate/device/invalidate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> str:
        """
        invalidate the device
        POST /dataservice/certificate/device/invalidate

        :param payload: Device UUID
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/device/invalidate",
            return_type=str,
            payload=payload,
            **kw,
        )
