# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class LinksBuilder:
    """
    Builds and executes requests for operations under /device/omp/links
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: str, **kw) -> Any:
        """
        Get OMP connection list
        GET /dataservice/device/omp/links

        :param state: Connection state
        :returns: Any
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/omp/links", params=params, **kw
        )
