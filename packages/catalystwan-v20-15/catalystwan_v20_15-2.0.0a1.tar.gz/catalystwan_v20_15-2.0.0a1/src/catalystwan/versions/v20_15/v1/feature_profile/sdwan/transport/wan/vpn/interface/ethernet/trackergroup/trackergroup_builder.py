# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceEthernetTrackergroupPayload,
    GetWanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse,
)


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        trackergroup_id: str,
        payload: EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceEthernet parcel and a TrackerGroup Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup ID
        :param payload: TrackerGroup Profile Parcel
        :returns: EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
            return_type=EditWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ethernet_id: str, trackergroup_id: str, **kw):
        """
        Delete a WanVpnInterfaceEthernet and a TrackerGroup Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceEthernet parcel with a TrackerGroup Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel Id
        :returns: CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/trackergroup",
            return_type=CreateWanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, trackergroup_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceEthernetTrackergroupPayload:
        """
        Get WanVpnInterfaceEthernet associated TrackerGroup Parcel by trackergroupId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceEthernetTrackergroupPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetWanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceEthernet associated TrackerGroup Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        trackergroup_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceEthernetTrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str), (trackergroup_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "trackergroupId": trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceEthernetTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str)], [trackergroup_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup",
                return_type=List[
                    GetWanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
