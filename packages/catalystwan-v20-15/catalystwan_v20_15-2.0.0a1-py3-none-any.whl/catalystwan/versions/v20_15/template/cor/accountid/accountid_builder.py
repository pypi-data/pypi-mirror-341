# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class AccountidBuilder:
    """
    Builds and executes requests for operations under /template/cor/accountid
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(
        self,
        accountid: str,
        transitvpcid: str,
        cloudregion: str,
        cloudtype: Optional[str] = "AWS",
        **kw,
    ) -> Any:
        """
        Delete transit VPC/VNet
        DELETE /dataservice/template/cor/accountid/{accountid}

        :param accountid: Account Id
        :param transitvpcid: Cloud VPC Id
        :param cloudregion: Cloud region
        :param cloudtype: Cloud type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "removeTransitVPC")
        params = {
            "accountid": accountid,
            "transitvpcid": transitvpcid,
            "cloudregion": cloudregion,
            "cloudtype": cloudtype,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/cor/accountid/{accountid}", params=params, **kw
        )
