# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceSviParcelForServicePostRequest,
    CreateLanVpnInterfaceSviParcelForServicePostResponse,
    EditLanVpnInterfaceSviParcelForServicePutRequest,
    EditLanVpnInterfaceSviParcelForServicePutResponse,
    GetListSdwanServiceLanVpnInterfaceSviPayload,
    GetSingleSdwanServiceLanVpnInterfaceSviPayload,
)

if TYPE_CHECKING:
    from .dhcp_server.dhcp_server_builder import DhcpServerBuilder
    from .schema.schema_builder import SchemaBuilder


class SviBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn/interface/svi
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnInterfaceSviParcelForServicePostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceSviParcelForServicePostResponse:
        """
        Create a LanVpn InterfaceSvi parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Lan Vpn Interface Svi Profile Parcel
        :returns: CreateLanVpnInterfaceSviParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi",
            return_type=CreateLanVpnInterfaceSviParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        svi_id: str,
        payload: EditLanVpnInterfaceSviParcelForServicePutRequest,
        **kw,
    ) -> EditLanVpnInterfaceSviParcelForServicePutResponse:
        """
        Update a LanVpn InterfaceSvi Parcel for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param svi_id: Interface ID
        :param payload: Lan Vpn Interface Svi Profile Parcel
        :returns: EditLanVpnInterfaceSviParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "sviId": svi_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}",
            return_type=EditLanVpnInterfaceSviParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, svi_id: str, **kw):
        """
        Delete a  LanVpn InterfaceSvi Parcel for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param svi_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "sviId": svi_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, svi_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceSviPayload:
        """
        Get LanVpn InterfaceSvi Parcel by sviId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param svi_id: Interface Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceSviPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> GetListSdwanServiceLanVpnInterfaceSviPayload:
        """
        Get InterfaceSvi Parcels for service LanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanServiceLanVpnInterfaceSviPayload
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, svi_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceLanVpnInterfaceSviPayload, GetSingleSdwanServiceLanVpnInterfaceSviPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (svi_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "sviId": svi_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi/{sviId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceSviPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [svi_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/svi",
                return_type=GetListSdwanServiceLanVpnInterfaceSviPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def dhcp_server(self) -> DhcpServerBuilder:
        """
        The dhcp-server property
        """
        from .dhcp_server.dhcp_server_builder import DhcpServerBuilder

        return DhcpServerBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
