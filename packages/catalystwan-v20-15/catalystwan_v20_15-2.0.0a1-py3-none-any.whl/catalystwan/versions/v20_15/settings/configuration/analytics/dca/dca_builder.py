# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DcaBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/analytics/dca
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> str:
        """
        Create analytics data file
        POST /dataservice/settings/configuration/analytics/dca

        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/settings/configuration/analytics/dca", return_type=str, **kw
        )
