# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostRequest,
    CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse,
    EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutRequest,
    EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse,
    GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse,
    GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        tracker_id: str,
        payload: EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a LanVpnInterfaceEthernet parcel and a Tracker Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
            return_type=EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ethernet_id: str, tracker_id: str, **kw):
        """
        Delete a LanVpnInterfaceEthernet and a Tracker Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        service_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a LanVpnInterfaceEthernet parcel with a Tracker Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/tracker

        :param service_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/tracker",
            return_type=CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload:
        """
        Get LanVpnInterfaceEthernet associated Tracker Parcel by trackerId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get LanVpnInterfaceEthernet associated Tracker Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str), (tracker_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str)], [tracker_id]
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker",
                return_type=List[
                    GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
