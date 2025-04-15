# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AccountBuilder:
    """
    Builds and executes requests for operations under /template/cor/cloud/account
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloudtype: str, cloud_environment: str, **kw) -> Any:
        """
        Get cloud accounts
        GET /dataservice/template/cor/cloud/account

        :param cloudtype: Cloud type
        :param cloud_environment: Cloud environment
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudAccounts")
        params = {
            "cloudtype": cloudtype,
            "cloudEnvironment": cloud_environment,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/cloud/account", params=params, **kw
        )
