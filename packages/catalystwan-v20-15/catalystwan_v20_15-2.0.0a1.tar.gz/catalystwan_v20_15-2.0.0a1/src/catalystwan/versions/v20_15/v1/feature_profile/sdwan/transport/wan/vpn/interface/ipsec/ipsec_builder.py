# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateIpSecProfileParcel1PostRequest,
    CreateIpSecProfileParcel1PostResponse,
    EditProfileParcel1PutRequest,
    EditProfileParcel1PutResponse,
    GetListSdwanTransportWanVpnInterfaceIpsecPayload,
    GetSingleSdwanTransportWanVpnInterfaceIpsecPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder
    from .tracker.tracker_builder import TrackerBuilder


class IpsecBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/ipsec
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, vpn_id: str, payload: CreateIpSecProfileParcel1PostRequest, **kw
    ) -> CreateIpSecProfileParcel1PostResponse:
        """
        Create a WanVpn InterfaceIpsec parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Interface Ethernet Profile Parcel
        :returns: CreateIpSecProfileParcel1PostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec",
            return_type=CreateIpSecProfileParcel1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ipsec_id: str,
        payload: EditProfileParcel1PutRequest,
        **kw,
    ) -> EditProfileParcel1PutResponse:
        """
        Update a WanVpn InterfaceIpsec Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface ID
        :param payload: Wan Vpn Interface Ipsec Profile Parcel
        :returns: EditProfileParcel1PutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
            return_type=EditProfileParcel1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ipsec_id: str, **kw):
        """
        Delete a  WanVpn InterfaceIpsec Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ipsec_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceIpsecPayload:
        """
        Get WanVpn InterfaceIpsec Parcel by ethernetId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceIpsecPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportWanVpnInterfaceIpsecPayload:
        """
        Get InterfaceIpsec Parcels for transport WanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportWanVpnInterfaceIpsecPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ipsec_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportWanVpnInterfaceIpsecPayload,
        GetSingleSdwanTransportWanVpnInterfaceIpsecPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ipsec_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [ipsec_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec",
                return_type=GetListSdwanTransportWanVpnInterfaceIpsecPayload,
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

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)
