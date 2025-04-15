# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FieldsBuilder:
    """
    Builds and executes requests for operations under /alarms/query/fields
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get query fields
        GET /dataservice/alarms/query/fields

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/alarms/query/fields", **kw)
