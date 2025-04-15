# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /util/olapdb/migration/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get migration status
        GET /dataservice/util/olapdb/migration/status

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/util/olapdb/migration/status", **kw
        )
