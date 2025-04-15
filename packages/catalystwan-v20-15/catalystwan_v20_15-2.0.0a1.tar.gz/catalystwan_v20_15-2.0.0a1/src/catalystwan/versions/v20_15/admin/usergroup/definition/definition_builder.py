# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DefinitionBuilder:
    """
    Builds and executes requests for operations under /admin/usergroup/definition
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get user groups in a grid table
        GET /dataservice/admin/usergroup/definition

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/admin/usergroup/definition", **kw)
