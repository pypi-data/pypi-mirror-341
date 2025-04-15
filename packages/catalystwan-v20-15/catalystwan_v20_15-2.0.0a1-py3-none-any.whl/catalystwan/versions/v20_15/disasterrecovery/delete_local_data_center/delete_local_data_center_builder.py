# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DeleteLocalDataCenterBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/deleteLocalDataCenter
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Delete local data center
        POST /dataservice/disasterrecovery/deleteLocalDataCenter

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/deleteLocalDataCenter", **kw
        )
