# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ListenersBuilder:
    """
    Builds and executes requests for operations under /event/listeners
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Retrieve listener information
        GET /dataservice/event/listeners

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/event/listeners", return_type=str, **kw
        )
