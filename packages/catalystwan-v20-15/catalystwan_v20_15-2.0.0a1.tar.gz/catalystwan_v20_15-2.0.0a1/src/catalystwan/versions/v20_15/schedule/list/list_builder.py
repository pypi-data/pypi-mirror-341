# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /schedule/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, limit: Optional[int] = 100, **kw) -> Any:
        """
        Get a schedule record for backup by scheduler id
        GET /dataservice/schedule/list

        :param limit: size
        :returns: Any
        """
        params = {
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/schedule/list", params=params, **kw
        )
