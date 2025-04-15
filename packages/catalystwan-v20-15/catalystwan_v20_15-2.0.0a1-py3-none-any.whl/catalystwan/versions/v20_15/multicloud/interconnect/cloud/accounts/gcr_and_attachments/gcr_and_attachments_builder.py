# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, InlineResponse20010


class GcrAndAttachmentsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/gcr-and-attachments
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: CloudTypeParam,
        cloud_account_id: str,
        connectivity_gateway_name: Optional[str] = None,
        cloud_gateway_name: Optional[str] = None,
        region: Optional[str] = None,
        network: Optional[str] = None,
        resource_state: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> InlineResponse20010:
        """
        API to get Google Cloud Router and Attachments.
        GET /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/gcr-and-attachments

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param connectivity_gateway_name: Connectivity gateway name
        :param cloud_gateway_name: Cloud gateway name
        :param region: Region
        :param network: Network
        :param resource_state: Resource state
        :param refresh: Refresh
        :returns: InlineResponse20010
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "connectivity-gateway-name": connectivity_gateway_name,
            "cloud-gateway-name": cloud_gateway_name,
            "region": region,
            "network": network,
            "resource-state": resource_state,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/gcr-and-attachments",
            return_type=InlineResponse20010,
            params=params,
            **kw,
        )
