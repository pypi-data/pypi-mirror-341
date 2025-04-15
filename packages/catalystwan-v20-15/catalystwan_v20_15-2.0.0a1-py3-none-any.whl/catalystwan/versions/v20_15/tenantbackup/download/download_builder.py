# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /tenantbackup/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, path: str, **kw) -> Any:
        """
        Download a Backup File that is already stored in vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenantbackup/download/{path}

        :param path: File path
        :returns: Any
        """
        params = {
            "path": path,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/tenantbackup/download/{path}", params=params, **kw
        )
