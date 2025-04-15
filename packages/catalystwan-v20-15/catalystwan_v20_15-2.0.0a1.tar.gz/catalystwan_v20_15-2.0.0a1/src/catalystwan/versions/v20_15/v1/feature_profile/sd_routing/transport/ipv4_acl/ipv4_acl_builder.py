# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportIpv4AclFeaturePostRequest,
    CreateSdroutingTransportIpv4AclFeaturePostResponse,
    EditSdroutingTransportIpv4AclFeaturePutRequest,
    EditSdroutingTransportIpv4AclFeaturePutResponse,
    GetListSdRoutingTransportIpv4AclPayload,
    GetSingleSdRoutingTransportIpv4AclPayload,
)


class Ipv4AclBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateSdroutingTransportIpv4AclFeaturePostRequest, **kw
    ) -> CreateSdroutingTransportIpv4AclFeaturePostResponse:
        """
        Create a SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        :returns: CreateSdroutingTransportIpv4AclFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl",
            return_type=CreateSdroutingTransportIpv4AclFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ipv4_acl_id: str,
        payload: EditSdroutingTransportIpv4AclFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportIpv4AclFeaturePutResponse:
        """
        Edit a SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}

        :param transport_id: Transport Profile ID
        :param ipv4_acl_id: Ipv4 ACL Feature ID
        :param payload: SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        :returns: EditSdroutingTransportIpv4AclFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "ipv4AclId": ipv4_acl_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}",
            return_type=EditSdroutingTransportIpv4AclFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ipv4_acl_id: str, **kw):
        """
        Delete a SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}

        :param transport_id: Transport Profile ID
        :param ipv4_acl_id: IPv4 ACL Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ipv4AclId": ipv4_acl_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ipv4_acl_id: str, **kw
    ) -> GetSingleSdRoutingTransportIpv4AclPayload:
        """
        Get a SD-Routing Ipv4 Acl Feature for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}

        :param transport_id: Transport Profile ID
        :param ipv4_acl_id: IPv4 ACL Feature ID
        :returns: GetSingleSdRoutingTransportIpv4AclPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportIpv4AclPayload:
        """
        Get all SD-Routing Ipv4 Acl Features for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportIpv4AclPayload
        """
        ...

    def get(
        self, transport_id: str, ipv4_acl_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingTransportIpv4AclPayload, GetSingleSdRoutingTransportIpv4AclPayload]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}
        if self._request_adapter.param_checker([(transport_id, str), (ipv4_acl_id, str)], []):
            params = {
                "transportId": transport_id,
                "ipv4AclId": ipv4_acl_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl/{ipv4AclId}",
                return_type=GetSingleSdRoutingTransportIpv4AclPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl
        if self._request_adapter.param_checker([(transport_id, str)], [ipv4_acl_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/ipv4-acl",
                return_type=GetListSdRoutingTransportIpv4AclPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
