# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /certificate/stats/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[str]:
        """
        Get certificate expiration status
        GET /dataservice/certificate/stats/summary

        :returns: List[str]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/stats/summary", return_type=List[str], **kw
        )
