# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ErrorsBuilder:
    """
    Builds and executes requests for operations under /device/hardware/errors
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get hardware error list from device
        GET /dataservice/device/hardware/errors

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/hardware/errors", **kw)
