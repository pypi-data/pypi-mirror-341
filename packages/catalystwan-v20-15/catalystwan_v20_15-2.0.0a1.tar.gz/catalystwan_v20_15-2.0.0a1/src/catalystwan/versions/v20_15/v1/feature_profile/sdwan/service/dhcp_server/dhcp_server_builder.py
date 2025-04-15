# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateDhcpServerProfileParcelForServicePostRequest,
    CreateDhcpServerProfileParcelForServicePostResponse,
    EditDhcpServerProfileParcelForServicePutRequest,
    EditDhcpServerProfileParcelForServicePutResponse,
    GetListSdwanServiceDhcpServerPayload,
    GetSingleSdwanServiceDhcpServerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class DhcpServerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/dhcp-server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateDhcpServerProfileParcelForServicePostRequest, **kw
    ) -> CreateDhcpServerProfileParcelForServicePostResponse:
        """
        Create a Dhcp Server Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server

        :param service_id: Feature Profile ID
        :param payload: Dhcp Server Profile Parcel
        :returns: CreateDhcpServerProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server",
            return_type=CreateDhcpServerProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        dhcp_server_id: str,
        payload: EditDhcpServerProfileParcelForServicePutRequest,
        **kw,
    ) -> EditDhcpServerProfileParcelForServicePutResponse:
        """
        Update a Dhcp Server Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param dhcp_server_id: Profile Parcel ID
        :param payload: Dhcp Server Profile Parcel
        :returns: EditDhcpServerProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}",
            return_type=EditDhcpServerProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, dhcp_server_id: str, **kw):
        """
        Delete a Dhcp Server Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param dhcp_server_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, dhcp_server_id: str, **kw
    ) -> GetSingleSdwanServiceDhcpServerPayload:
        """
        Get Dhcp Server Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param dhcp_server_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceDhcpServerPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceDhcpServerPayload:
        """
        Get Dhcp Server Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceDhcpServerPayload
        """
        ...

    def get(
        self, service_id: str, dhcp_server_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceDhcpServerPayload, GetSingleSdwanServiceDhcpServerPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}
        if self._request_adapter.param_checker([(service_id, str), (dhcp_server_id, str)], []):
            params = {
                "serviceId": service_id,
                "dhcpServerId": dhcp_server_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server/{dhcpServerId}",
                return_type=GetSingleSdwanServiceDhcpServerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server
        if self._request_adapter.param_checker([(service_id, str)], [dhcp_server_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/dhcp-server",
                return_type=GetListSdwanServiceDhcpServerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
