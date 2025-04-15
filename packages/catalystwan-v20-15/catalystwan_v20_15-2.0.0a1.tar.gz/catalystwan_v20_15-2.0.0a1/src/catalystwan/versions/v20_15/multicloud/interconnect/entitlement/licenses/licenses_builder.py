# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectLicense


class LicensesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/entitlement/licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: str,
        interconnect_account_id: str,
        refresh: Optional[str] = "false",
        product_type: Optional[str] = None,
        **kw,
    ) -> List[InterconnectLicense]:
        """
        API to retrieve Interconnect licences
        GET /dataservice/multicloud/interconnect/entitlement/licenses

        :param interconnect_type: Interconnect provider type
        :param interconnect_account_id: Interconnect account id
        :param refresh: Refresh
        :param product_type: Interconnect License Product Type
        :returns: List[InterconnectLicense]
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-account-id": interconnect_account_id,
            "refresh": refresh,
            "product-type": product_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/entitlement/licenses",
            return_type=List[InterconnectLicense],
            params=params,
            **kw,
        )
