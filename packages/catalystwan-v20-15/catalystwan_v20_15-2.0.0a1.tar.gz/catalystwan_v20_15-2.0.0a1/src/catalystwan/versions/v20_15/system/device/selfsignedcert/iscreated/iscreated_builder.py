# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IscreatedBuilder:
    """
    Builds and executes requests for operations under /system/device/selfsignedcert/iscreated
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Whether self signed certificate created
        GET /dataservice/system/device/selfsignedcert/iscreated

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/system/device/selfsignedcert/iscreated", **kw
        )
