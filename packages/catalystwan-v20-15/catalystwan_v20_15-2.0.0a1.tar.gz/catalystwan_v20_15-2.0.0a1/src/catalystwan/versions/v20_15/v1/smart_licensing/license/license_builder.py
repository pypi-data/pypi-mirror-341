# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetLicenseResponseInner


class LicenseBuilder:
    """
    Builds and executes requests for operations under /v1/smart-licensing/license
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, virtual_account_id: str, license_type: str, **kw
    ) -> List[GetLicenseResponseInner]:
        """
        Get licenses from vManage db
        GET /dataservice/v1/smart-licensing/license

        :param virtual_account_id: virtual_account_id
        :param license_type: License type 'prepaid' or 'postpaid'
        :returns: List[GetLicenseResponseInner]
        """
        params = {
            "virtual_account_id": virtual_account_id,
            "licenseType": license_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/smart-licensing/license",
            return_type=List[GetLicenseResponseInner],
            params=params,
            **kw,
        )
