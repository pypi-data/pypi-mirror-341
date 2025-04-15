# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ComplianceBuilder:
    """
    Builds and executes requests for operations under /msla/licenses/compliance
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Retrieve list of devices and their subscription information
        GET /dataservice/msla/licenses/compliance

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/msla/licenses/compliance", return_type=List[Any], **kw
        )
