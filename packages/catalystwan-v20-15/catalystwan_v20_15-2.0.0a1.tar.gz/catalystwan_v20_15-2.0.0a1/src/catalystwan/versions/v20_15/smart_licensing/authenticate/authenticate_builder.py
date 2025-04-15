# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AuthenticateBuilder:
    """
    Builds and executes requests for operations under /smartLicensing/authenticate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        authenticate user for sle
        POST /dataservice/smartLicensing/authenticate

        :param payload: Partner
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/smartLicensing/authenticate", payload=payload, **kw
        )
