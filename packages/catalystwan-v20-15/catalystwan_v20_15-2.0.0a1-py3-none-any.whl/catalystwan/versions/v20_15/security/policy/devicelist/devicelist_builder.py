# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SecurityPolicyDeviceList


class DevicelistBuilder:
    """
    Builds and executes requests for operations under /security/policy/devicelist
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[SecurityPolicyDeviceList]:
        """
        Get security policy device list
        GET /dataservice/security/policy/devicelist

        :returns: List[SecurityPolicyDeviceList]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/security/policy/devicelist",
            return_type=List[SecurityPolicyDeviceList],
            **kw,
        )
