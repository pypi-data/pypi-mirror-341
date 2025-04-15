# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /template/policy/security/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Generate security policy summary
        GET /dataservice/template/policy/security/summary

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/security/summary", **kw
        )
