# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2001


class BillingAccountsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/billing-accounts
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: str,
        interconnect_account_id: str,
        region: Optional[str] = None,
        **kw,
    ) -> InlineResponse2001:
        """
        API to retrieve billing accounts for an Interconnect provider type and account.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/billing-accounts

        :param interconnect_type: Interconnect provider type
        :param interconnect_account_id: Interconnect provider account id
        :param region: Region
        :returns: InlineResponse2001
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-account-id": interconnect_account_id,
            "region": region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/billing-accounts",
            return_type=InlineResponse2001,
            params=params,
            **kw,
        )
