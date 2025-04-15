# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintech/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, filename: str, **kw):
        """
        Download admin tech logs
        GET /dataservice/device/tools/admintech/download/{filename}

        :param filename: Admin tech file
        :returns: None
        """
        params = {
            "filename": filename,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/tools/admintech/download/{filename}", params=params, **kw
        )
