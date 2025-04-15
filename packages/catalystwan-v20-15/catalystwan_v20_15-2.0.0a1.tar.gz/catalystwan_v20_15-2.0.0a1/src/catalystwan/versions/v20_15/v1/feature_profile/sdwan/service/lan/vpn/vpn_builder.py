# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnProfileParcelForServicePostRequest,
    CreateLanVpnProfileParcelForServicePostResponse,
    EditLanVpnProfileParcelForServicePutRequest,
    EditLanVpnProfileParcelForServicePutResponse,
    GetListSdwanServiceLanVpnPayload,
    GetSingleSdwanServiceLanVpnPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .routing.routing_builder import RoutingBuilder
    from .schema.schema_builder import SchemaBuilder


class VpnBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateLanVpnProfileParcelForServicePostRequest, **kw
    ) -> CreateLanVpnProfileParcelForServicePostResponse:
        """
        Create a Lan Vpn Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn

        :param service_id: Feature Profile ID
        :param payload: Lan Vpn Profile Parcel
        :returns: CreateLanVpnProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn",
            return_type=CreateLanVpnProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        payload: EditLanVpnProfileParcelForServicePutRequest,
        **kw,
    ) -> EditLanVpnProfileParcelForServicePutResponse:
        """
        Update a Lan Vpn Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Lan Vpn Profile Parcel
        :returns: EditLanVpnProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}",
            return_type=EditLanVpnProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, **kw):
        """
        Delete a Lan Vpn Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, vpn_id: str, **kw) -> GetSingleSdwanServiceLanVpnPayload:
        """
        Get Lan Vpn Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceLanVpnPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceLanVpnPayload:
        """
        Get Lan Vpn Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceLanVpnPayload
        """
        ...

    def get(
        self, service_id: str, vpn_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceLanVpnPayload, GetSingleSdwanServiceLanVpnPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], []):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}",
                return_type=GetSingleSdwanServiceLanVpnPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn
        if self._request_adapter.param_checker([(service_id, str)], [vpn_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn",
                return_type=GetListSdwanServiceLanVpnPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
