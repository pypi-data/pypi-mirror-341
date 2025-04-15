# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /certificate/list/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[str]:
        """
        get certificate data
        GET /dataservice/certificate/list/status

        :returns: List[str]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/list/status", return_type=List[str], **kw
        )
