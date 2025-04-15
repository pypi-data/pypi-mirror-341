# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetHsecDevicesPayloadInner


class InstallBuilder:
    """
    Builds and executes requests for operations under /hsec/devices/install
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GetHsecDevicesPayloadInner]:
        """
        Retrieve list of devices which has HSEC fetched
        GET /dataservice/hsec/devices/install

        :returns: List[GetHsecDevicesPayloadInner]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/hsec/devices/install",
            return_type=List[GetHsecDevicesPayloadInner],
            **kw,
        )
