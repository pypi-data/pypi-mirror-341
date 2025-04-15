# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VersionBuilder:
    """
    Builds and executes requests for operations under /device/action/software/ztp/version
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get ZTP software version
        GET /dataservice/device/action/software/ztp/version

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/software/ztp/version", **kw
        )
