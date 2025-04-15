# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class MigrationBuilder:
    """
    Builds and executes requests for operations under /template/feature/migration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Generate a list of templates which require migration


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/feature/migration

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/feature/migration", return_type=List[Any], **kw
        )
