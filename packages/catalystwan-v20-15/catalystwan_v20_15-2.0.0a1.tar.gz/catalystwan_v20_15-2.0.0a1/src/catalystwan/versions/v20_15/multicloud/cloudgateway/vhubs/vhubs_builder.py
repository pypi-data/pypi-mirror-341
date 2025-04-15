# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VhubsListResponse


class VhubsBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/vhubs
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        account_id: str,
        region: str,
        resource_group_name: str,
        resource_group_source: str,
        vwan_name: str,
        vwan_source: str,
        **kw,
    ) -> List[VhubsListResponse]:
        """
        Discover Azure Virtual HUBs
        GET /dataservice/multicloud/cloudgateway/vhubs

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param region: Region
        :param resource_group_name: Resource group name
        :param resource_group_source: Resource group source
        :param vwan_name: Vwan name
        :param vwan_source: Vwan source
        :returns: List[VhubsListResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "region": region,
            "resourceGroupName": resource_group_name,
            "resourceGroupSource": resource_group_source,
            "vwanName": vwan_name,
            "vwanSource": vwan_source,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/vhubs",
            return_type=List[VhubsListResponse],
            params=params,
            **kw,
        )
