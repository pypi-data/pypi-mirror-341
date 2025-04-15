# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CategoryBuilder:
    """
    Builds and executes requests for operations under /app-registry/app/category
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get the stats of all type of apps
        GET /dataservice/app-registry/app/category

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/app-registry/app/category", return_type=List[Any], **kw
        )
