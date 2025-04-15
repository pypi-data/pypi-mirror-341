# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/partnerports/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        edge_type: Optional[EdgeTypeParam] = None,
        account_id: Optional[str] = None,
        cloud_type: Optional[str] = None,
        connect_type: Optional[str] = None,
        vxc_permitted: Optional[str] = None,
        authorization_key: Optional[str] = None,
        refresh: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get partner ports
        GET /dataservice/multicloud/partnerports/edge

        :param edge_type: Edge type
        :param account_id: Edge Account Id
        :param cloud_type: Cloud Type
        :param connect_type: Connect Type filter
        :param vxc_permitted: VXC Permitted on the port
        :param authorization_key: authorization Key
        :param refresh: Refresh
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getPartnerPorts")
        params = {
            "edgeType": edge_type,
            "accountId": account_id,
            "cloudType": cloud_type,
            "connectType": connect_type,
            "vxcPermitted": vxc_permitted,
            "authorizationKey": authorization_key,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/partnerports/edge", params=params, **kw
        )
