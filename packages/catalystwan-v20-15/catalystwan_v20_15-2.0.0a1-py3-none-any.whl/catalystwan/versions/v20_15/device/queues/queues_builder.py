# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class QueuesBuilder:
    """
    Builds and executes requests for operations under /device/queues
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get synchronized queue information, returns information about syncing, queued and stuck devices
        GET /dataservice/device/queues

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/queues", **kw)
