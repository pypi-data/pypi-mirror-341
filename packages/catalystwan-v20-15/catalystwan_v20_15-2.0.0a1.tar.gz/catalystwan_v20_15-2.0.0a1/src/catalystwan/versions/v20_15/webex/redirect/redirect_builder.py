# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import RedirectCodeResponse


class RedirectBuilder:
    """
    Builds and executes requests for operations under /webex/redirect
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, code: str, **kw) -> RedirectCodeResponse:
        """
        Redirect Info
        GET /dataservice/webex/redirect

        :param code: code
        :returns: RedirectCodeResponse
        """
        params = {
            "code": code,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/webex/redirect",
            return_type=RedirectCodeResponse,
            params=params,
            **kw,
        )
