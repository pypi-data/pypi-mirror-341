# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StagingBuilder:
    """
    Builds and executes requests for operations under /cloudservices/staging
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Check if testbed or production
        GET /dataservice/cloudservices/staging

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/cloudservices/staging", **kw)
