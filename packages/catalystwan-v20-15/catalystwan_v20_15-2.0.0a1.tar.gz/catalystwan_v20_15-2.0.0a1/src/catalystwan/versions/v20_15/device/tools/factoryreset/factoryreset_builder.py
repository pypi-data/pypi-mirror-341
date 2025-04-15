# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FactoryresetBuilder:
    """
    Builds and executes requests for operations under /device/tools/factoryreset
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Device factory reset
        POST /dataservice/device/tools/factoryreset

        :param payload: Device factory reset
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/tools/factoryreset", payload=payload, **kw
        )
