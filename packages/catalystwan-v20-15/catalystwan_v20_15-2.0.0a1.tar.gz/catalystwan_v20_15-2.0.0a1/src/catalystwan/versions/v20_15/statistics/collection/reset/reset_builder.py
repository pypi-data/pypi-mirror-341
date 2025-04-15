# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ResetBuilder:
    """
    Builds and executes requests for operations under /statistics/collection/reset
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, process_queue: int, **kw) -> Any:
        """
        Reset stats collect thread report
        GET /dataservice/statistics/collection/reset/{processQueue}

        :param process_queue: Process queue
        :returns: Any
        """
        params = {
            "processQueue": process_queue,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/collection/reset/{processQueue}", params=params, **kw
        )
