# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ClientSessionTimeoutBuilder:
    """
    Builds and executes requests for operations under /settings/clientSessionTimeout
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Get client session timeout
        GET /dataservice/settings/clientSessionTimeout

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/settings/clientSessionTimeout", return_type=str, **kw
        )
