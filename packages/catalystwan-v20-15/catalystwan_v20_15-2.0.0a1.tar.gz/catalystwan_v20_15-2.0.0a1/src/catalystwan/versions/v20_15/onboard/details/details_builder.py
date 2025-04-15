# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceDetailsData


class DetailsBuilder:
    """
    Builds and executes requests for operations under /onboard/details
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: DeviceDetailsData, **kw):
        """
        Add Manual Onboard Device details
        POST /dataservice/onboard/details

        :param payload: On board Device details
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/onboard/details", payload=payload, **kw
        )
