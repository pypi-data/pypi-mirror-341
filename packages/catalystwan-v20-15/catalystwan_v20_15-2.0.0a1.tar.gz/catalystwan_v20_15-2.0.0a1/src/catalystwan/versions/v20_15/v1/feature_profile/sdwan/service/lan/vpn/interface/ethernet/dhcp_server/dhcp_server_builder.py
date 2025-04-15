# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostRequest,
    CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostResponse,
    EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutRequest,
    EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutResponse,
    GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse,
    GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload,
)


class DhcpServerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        dhcp_server_id: str,
        payload: EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutResponse:
        """
        Update a LanVpnInterfaceEthernet parcel and a DhcpServer Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer ID
        :param payload: DhcpServer Profile Parcel
        :returns: EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
            return_type=EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ethernet_id: str, dhcp_server_id: str, **kw):
        """
        Delete a LanVpnInterfaceEthernet and a DhcpServer Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        service_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostResponse:
        """
        Associate a LanVpnInterfaceEthernet parcel with a DhcpServer Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/dhcp-server

        :param service_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: DhcpServer Profile Parcel Id
        :returns: CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/dhcp-server",
            return_type=CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, dhcp_server_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload:
        """
        Get LanVpnInterfaceEthernet associated DhcpServer Parcel by dhcpServerId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse]:
        """
        Get LanVpnInterfaceEthernet associated DhcpServer Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        dhcp_server_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse],
        GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str), (dhcp_server_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "dhcpServerId": dhcp_server_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str)], [dhcp_server_id]
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/dhcp-server",
                return_type=List[
                    GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
