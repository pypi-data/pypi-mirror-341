# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ResourceGroupsResponse


class ResourceGroupsBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/resourceGroups
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: str, account_id: str, **kw) -> List[ResourceGroupsResponse]:
        """
        Discover Azure Resource Groups
        GET /dataservice/multicloud/cloudgateway/resourceGroups

        :param cloud_type: Multicloud provider type
        :param account_id: Multicloud account id
        :returns: List[ResourceGroupsResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/resourceGroups",
            return_type=List[ResourceGroupsResponse],
            params=params,
            **kw,
        )
