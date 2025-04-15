# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /hsec/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Download SLAC Request file for CSSM
        POST /dataservice/hsec/download

        :param payload: Device List
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/hsec/download", payload=payload, **kw
        )
