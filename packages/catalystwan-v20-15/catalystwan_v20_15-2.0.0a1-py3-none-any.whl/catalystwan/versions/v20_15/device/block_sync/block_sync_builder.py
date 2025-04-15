# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class BlockSyncBuilder:
    """
    Builds and executes requests for operations under /device/blockSync
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, block_sync: str, **kw) -> Any:
        """
        Set collection manager block set flag
        POST /dataservice/device/blockSync

        :param block_sync: Block sync flag
        :returns: Any
        """
        params = {
            "blockSync": block_sync,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/device/blockSync", params=params, **kw
        )
