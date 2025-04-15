# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InitBlob


class InitBuilder:
    """
    Builds and executes requests for operations under /aas/init
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: InitBlob, **kw):
        """
        Initialize SDWAN as a Platform
        POST /dataservice/aas/init

        :param payload: Payload
        :returns: None
        """
        return self._request_adapter.request("POST", "/dataservice/aas/init", payload=payload, **kw)
