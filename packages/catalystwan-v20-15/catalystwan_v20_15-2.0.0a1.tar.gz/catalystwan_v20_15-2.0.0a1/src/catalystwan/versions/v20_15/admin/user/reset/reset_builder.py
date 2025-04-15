# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ResetBuilder:
    """
    Builds and executes requests for operations under /admin/user/reset
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Unlock a user
        POST /dataservice/admin/user/reset

        :param payload: User
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/user/reset", payload=payload, **kw
        )
