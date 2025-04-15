# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ActivateBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/activate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Activate cluster to start working as primary
        POST /dataservice/disasterrecovery/activate

        :returns: Any
        """
        return self._request_adapter.request("POST", "/dataservice/disasterrecovery/activate", **kw)
