# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /fedramp/wazuh/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get Wazuh agent status
        GET /dataservice/fedramp/wazuh/status

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/fedramp/wazuh/status", return_type=List[Any], **kw
        )
