# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UnpausereplicationBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/unpausereplication
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Un-Pause DR data replication
        POST /dataservice/disasterrecovery/unpausereplication

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "disasterRecoveryUnPauseReplication")
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/unpausereplication", **kw
        )
