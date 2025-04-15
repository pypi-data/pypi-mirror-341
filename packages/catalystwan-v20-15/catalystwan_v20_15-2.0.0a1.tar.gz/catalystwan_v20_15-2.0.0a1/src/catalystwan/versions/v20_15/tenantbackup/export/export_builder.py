# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ExportBuilder:
    """
    Builds and executes requests for operations under /tenantbackup/export
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Trigger a backup of configuration database and store it in vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenantbackup/export

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/tenantbackup/export", **kw)
