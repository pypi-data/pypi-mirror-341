# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceEthernetParcelForServicePostRequest,
    CreateLanVpnInterfaceEthernetParcelForServicePostResponse,
    EditLanVpnInterfaceEthernetParcelForServicePutRequest,
    EditLanVpnInterfaceEthernetParcelForServicePutResponse,
    GetListSdwanServiceLanVpnInterfaceEthernetPayload,
    GetSingleSdwanServiceLanVpnInterfaceEthernetPayload,
)

if TYPE_CHECKING:
    from .dhcp_server.dhcp_server_builder import DhcpServerBuilder
    from .schema.schema_builder import SchemaBuilder
    from .tracker.tracker_builder import TrackerBuilder
    from .trackergroup.trackergroup_builder import TrackergroupBuilder


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnInterfaceEthernetParcelForServicePostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceEthernetParcelForServicePostResponse:
        """
        Create a LanVpn InterfaceEthernet parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Lan Vpn Interface Ethernet Profile Parcel
        :returns: CreateLanVpnInterfaceEthernetParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet",
            return_type=CreateLanVpnInterfaceEthernetParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        payload: EditLanVpnInterfaceEthernetParcelForServicePutRequest,
        **kw,
    ) -> EditLanVpnInterfaceEthernetParcelForServicePutResponse:
        """
        Update a LanVpn InterfaceEthernet Parcel for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface ID
        :param payload: Lan Vpn Interface Ethernet Profile Parcel
        :returns: EditLanVpnInterfaceEthernetParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            return_type=EditLanVpnInterfaceEthernetParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ethernet_id: str, **kw):
        """
        Delete a  LanVpn InterfaceEthernet Parcel for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceEthernetPayload:
        """
        Get LanVpn InterfaceEthernet Parcel by ethernetId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> GetListSdwanServiceLanVpnInterfaceEthernetPayload:
        """
        Get InterfaceEthernet Parcels for service LanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanServiceLanVpnInterfaceEthernetPayload
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceLanVpnInterfaceEthernetPayload,
        GetSingleSdwanServiceLanVpnInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [ethernet_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet",
                return_type=GetListSdwanServiceLanVpnInterfaceEthernetPayload,
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

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)

    @property
    def trackergroup(self) -> TrackergroupBuilder:
        """
        The trackergroup property
        """
        from .trackergroup.trackergroup_builder import TrackergroupBuilder

        return TrackergroupBuilder(self._request_adapter)
