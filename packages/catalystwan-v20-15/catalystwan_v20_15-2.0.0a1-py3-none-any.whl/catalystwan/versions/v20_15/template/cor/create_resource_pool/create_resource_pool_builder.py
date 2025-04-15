# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CreateResourcePoolBuilder:
    """
    Builds and executes requests for operations under /template/cor/createResourcePool
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Add resource pool
        POST /dataservice/template/cor/createResourcePool

        :param payload: Add resource pool request
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "createResourcePool")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor/createResourcePool", payload=payload, **kw
        )
