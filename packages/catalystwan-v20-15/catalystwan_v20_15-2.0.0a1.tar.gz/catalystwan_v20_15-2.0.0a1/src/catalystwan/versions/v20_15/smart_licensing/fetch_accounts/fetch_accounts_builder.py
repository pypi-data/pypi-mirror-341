# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SmartLicensingfetchAccountsResp


class FetchAccountsBuilder:
    """
    Builds and executes requests for operations under /smartLicensing/fetchAccounts
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, mode: str, payload: Optional[Any] = None, **kw
    ) -> SmartLicensingfetchAccountsResp:
        """
        fetch sava for sle
        GET /dataservice/smartLicensing/fetchAccounts

        :param mode: mode
        :param payload: Partner
        :returns: SmartLicensingfetchAccountsResp
        """
        params = {
            "mode": mode,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/smartLicensing/fetchAccounts",
            return_type=SmartLicensingfetchAccountsResp,
            params=params,
            payload=payload,
            **kw,
        )
