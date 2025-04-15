# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class AmiBuilder:
    """
    Builds and executes requests for operations under /template/cor/ami
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, accountid: str, cloudregion: str, cloudtype: Optional[str] = "AWS", **kw
    ) -> List[Any]:
        """
        Get AMI list
        GET /dataservice/template/cor/ami

        :param accountid: Account Id
        :param cloudregion: Cloud region
        :param cloudtype: Cloud type
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getAmiList")
        params = {
            "accountid": accountid,
            "cloudregion": cloudregion,
            "cloudtype": cloudtype,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/ami", return_type=List[Any], params=params, **kw
        )
