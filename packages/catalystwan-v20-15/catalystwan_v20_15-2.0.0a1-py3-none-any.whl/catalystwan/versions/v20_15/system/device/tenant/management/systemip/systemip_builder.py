# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetTenantManagementSystemIPsInner


class SystemipBuilder:
    """
    Builds and executes requests for operations under /system/device/tenant/management/systemip
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GetTenantManagementSystemIPsInner]:
        """
        Get management system IP


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/system/device/tenant/management/systemip

        :returns: List[GetTenantManagementSystemIPsInner]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/tenant/management/systemip",
            return_type=List[GetTenantManagementSystemIPsInner],
            **kw,
        )
