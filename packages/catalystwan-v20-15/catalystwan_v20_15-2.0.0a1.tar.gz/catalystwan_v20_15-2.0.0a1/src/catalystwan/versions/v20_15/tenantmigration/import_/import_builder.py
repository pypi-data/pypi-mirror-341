# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ImportBuilder:
    """
    Builds and executes requests for operations under /tenantmigration/import
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, migration_key: str, **kw) -> Any:
        """
        Import tenant data
        POST /dataservice/tenantmigration/import/{migrationKey}

        :param migration_key: Migration key
        :returns: Any
        """
        params = {
            "migrationKey": migration_key,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/tenantmigration/import/{migrationKey}", params=params, **kw
        )
