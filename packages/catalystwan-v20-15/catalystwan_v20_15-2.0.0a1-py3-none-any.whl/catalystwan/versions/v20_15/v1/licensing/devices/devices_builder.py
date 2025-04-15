# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DevicesDetails


class DevicesBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DevicesDetails:
        """
        Retrieve list of all devices along with license details if assigned
        GET /dataservice/v1/licensing/devices

        :returns: DevicesDetails
        """
        return self._request_adapter.request(
            "GET", "/dataservice/v1/licensing/devices", return_type=DevicesDetails, **kw
        )
