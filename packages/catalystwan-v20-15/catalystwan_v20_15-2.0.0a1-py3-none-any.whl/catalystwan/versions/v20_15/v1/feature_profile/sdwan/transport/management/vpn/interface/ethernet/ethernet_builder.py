# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateManagementVpnInterfaceEthernetParcelForTransportPostRequest,
    CreateManagementVpnInterfaceEthernetParcelForTransportPostResponse,
    EditManagementVpnInterfaceEthernetParcelForTransportPutRequest,
    EditManagementVpnInterfaceEthernetParcelForTransportPutResponse,
    GetListSdwanTransportManagementVpnInterfaceEthernetPayload,
    GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/management/vpn/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateManagementVpnInterfaceEthernetParcelForTransportPostRequest,
        **kw,
    ) -> CreateManagementVpnInterfaceEthernetParcelForTransportPostResponse:
        """
        Create a ManagementVpn InterfaceEthernet parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Management Vpn Interface Ethernet Profile Parcel
        :returns: CreateManagementVpnInterfaceEthernetParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet",
            return_type=CreateManagementVpnInterfaceEthernetParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        payload: EditManagementVpnInterfaceEthernetParcelForTransportPutRequest,
        **kw,
    ) -> EditManagementVpnInterfaceEthernetParcelForTransportPutResponse:
        """
        Update a ManagementVpn InterfaceEthernet Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface ID
        :param payload: Management Vpn Interface Ethernet Profile Parcel
        :returns: EditManagementVpnInterfaceEthernetParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            return_type=EditManagementVpnInterfaceEthernetParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ethernet_id: str, **kw):
        """
        Delete a  ManagementVpn InterfaceEthernet Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload:
        """
        Get ManagementVpn InterfaceEthernet Parcel by ethernetId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportManagementVpnInterfaceEthernetPayload:
        """
        Get InterfaceEthernet Parcels for transport ManagementVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportManagementVpnInterfaceEthernetPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportManagementVpnInterfaceEthernetPayload,
        GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [ethernet_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}/interface/ethernet",
                return_type=GetListSdwanTransportManagementVpnInterfaceEthernetPayload,
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
