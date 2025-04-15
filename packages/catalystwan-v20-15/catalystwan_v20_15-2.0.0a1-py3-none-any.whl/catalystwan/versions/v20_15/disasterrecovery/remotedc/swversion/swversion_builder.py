# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SwversionBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/remotedc/swversion
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get remote data center vManage version
        GET /dataservice/disasterrecovery/remotedc/swversion

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/disasterrecovery/remotedc/swversion", **kw
        )
