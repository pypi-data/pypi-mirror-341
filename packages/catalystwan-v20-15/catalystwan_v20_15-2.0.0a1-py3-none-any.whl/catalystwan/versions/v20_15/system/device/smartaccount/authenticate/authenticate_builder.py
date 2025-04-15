# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SmartAccountAuthenticateResponse


class AuthenticateBuilder:
    """
    Builds and executes requests for operations under /system/device/smartaccount/authenticate
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> SmartAccountAuthenticateResponse:
        """
        Authenticate vSmart user account
        POST /dataservice/system/device/smartaccount/authenticate

        :param payload: Claim device request
        :returns: SmartAccountAuthenticateResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/smartaccount/authenticate",
            return_type=SmartAccountAuthenticateResponse,
            payload=payload,
            **kw,
        )
