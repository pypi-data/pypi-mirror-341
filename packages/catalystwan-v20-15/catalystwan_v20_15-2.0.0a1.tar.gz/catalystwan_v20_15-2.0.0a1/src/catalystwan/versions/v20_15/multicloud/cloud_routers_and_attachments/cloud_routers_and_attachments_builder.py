# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class CloudRoutersAndAttachmentsBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudRoutersAndAttachments
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        account_id: Optional[str] = None,
        region: Optional[str] = None,
        network: Optional[str] = None,
        connectivity_gateway_name: Optional[str] = None,
        cloud_gateway_name: Optional[str] = None,
        state: Optional[str] = None,
        refresh: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get all Cloud Routers and their Attachments
        GET /dataservice/multicloud/cloudRoutersAndAttachments

        :param account_id: Account Id
        :param region: Region
        :param network: Network
        :param connectivity_gateway_name: Connectivity Gateway Name
        :param cloud_gateway_name: Cloud Gateway Name
        :param state: State
        :param refresh: Refresh
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudRoutersAndAttachments")
        params = {
            "accountId": account_id,
            "region": region,
            "network": network,
            "connectivityGatewayName": connectivity_gateway_name,
            "cloudGatewayName": cloud_gateway_name,
            "state": state,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/cloudRoutersAndAttachments", params=params, **kw
        )
