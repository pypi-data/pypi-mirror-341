# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /certificate/mthub/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[str]:
        """
        vSmart Mthub list
        GET /dataservice/certificate/mthub/list

        :returns: List[str]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/mthub/list", return_type=List[str], **kw
        )
