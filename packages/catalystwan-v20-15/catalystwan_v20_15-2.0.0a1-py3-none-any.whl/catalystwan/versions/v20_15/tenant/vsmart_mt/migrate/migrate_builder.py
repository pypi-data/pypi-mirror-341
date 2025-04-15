# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class MigrateBuilder:
    """
    Builds and executes requests for operations under /tenant/vsmart-mt/migrate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> List[Any]:
        """
        Migrate tenants from single tenant vSmarts to multi-tenant capable vSmarts


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/tenant/vsmart-mt/migrate

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST", "/dataservice/tenant/vsmart-mt/migrate", return_type=List[Any], **kw
        )
