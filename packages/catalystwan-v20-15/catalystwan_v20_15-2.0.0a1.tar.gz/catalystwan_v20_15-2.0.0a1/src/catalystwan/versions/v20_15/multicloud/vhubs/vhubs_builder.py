# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class VhubsBuilder:
    """
    Builds and executes requests for operations under /multicloud/vhubs
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: Optional[str] = None,
        account_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        v_wan_name: Optional[str] = None,
        v_net_tags: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Virtual Hubs
        GET /dataservice/multicloud/vhubs

        :param cloud_type: Cloud Type
        :param account_id: Account Id
        :param resource_group: Resource Group
        :param v_wan_name: VWan Name
        :param v_net_tags: VNet Tags
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getVHubs")
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "resourceGroup": resource_group,
            "vWanName": v_wan_name,
            "vNetTags": v_net_tags,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/vhubs", params=params, **kw
        )
