# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ManagementBuilder:
    """
    Builds and executes requests for operations under /umbrella/getkeys/management
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get management keys from Umbrella
        GET /dataservice/umbrella/getkeys/management

        :returns: None
        """
        return self._request_adapter.request(
            "GET", "/dataservice/umbrella/getkeys/management", **kw
        )
