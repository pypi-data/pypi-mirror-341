# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SupportedResponse


class SupportedlistBuilder:
    """
    Builds and executes requests for operations under /onboard/supportedlist
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: List[str], **kw) -> SupportedResponse:
        """
        Manual Onboard Supported Device features
        POST /dataservice/onboard/supportedlist

        :param payload: Manual Onboard Supported Device
        :returns: SupportedResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/onboard/supportedlist",
            return_type=SupportedResponse,
            payload=payload,
            **kw,
        )
