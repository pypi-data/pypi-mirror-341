# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MappedhostaccountsBuilder:
    """
    Builds and executes requests for operations under /template/cor/cloud/mappedhostaccounts
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, accountid: str, cloudtype: str, **kw) -> Any:
        """
        Get cloud mapped accounts view
        GET /dataservice/template/cor/cloud/mappedhostaccounts

        :param accountid: Account Id
        :param cloudtype: Cloud type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudMappedHostAccounts")
        params = {
            "accountid": accountid,
            "cloudtype": cloudtype,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/cloud/mappedhostaccounts", params=params, **kw
        )
