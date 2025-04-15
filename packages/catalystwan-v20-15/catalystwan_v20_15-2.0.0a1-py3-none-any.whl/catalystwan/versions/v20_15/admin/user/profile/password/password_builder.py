# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PasswordBuilder:
    """
    Builds and executes requests for operations under /admin/user/profile/password
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw):
        """
        Update profile password
        PUT /dataservice/admin/user/profile/password

        :param payload: User
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/admin/user/profile/password", payload=payload, **kw
        )
