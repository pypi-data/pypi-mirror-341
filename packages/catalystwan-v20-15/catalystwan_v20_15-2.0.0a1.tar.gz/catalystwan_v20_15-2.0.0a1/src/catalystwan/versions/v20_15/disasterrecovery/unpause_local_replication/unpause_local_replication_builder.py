# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UnpauseLocalReplicationBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/unpauseLocalReplication
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Unpause DR replication for local datacenter
        POST /dataservice/disasterrecovery/unpauseLocalReplication

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/unpauseLocalReplication", **kw
        )
