# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class PemBuilder:
    """
    Builds and executes requests for operations under /template/cor/pem
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, accountid: str, cloudregion: str, cloudtype: str, **kw) -> List[Any]:
        """
        Get transit VPC PEM key list
        GET /dataservice/template/cor/pem

        :param accountid: Account Id
        :param cloudregion: Cloud region
        :param cloudtype: Cloud type
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getPemKeyList")
        params = {
            "accountid": accountid,
            "cloudregion": cloudregion,
            "cloudtype": cloudtype,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/pem", return_type=List[Any], params=params, **kw
        )
