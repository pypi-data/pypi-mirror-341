# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackerPayload,
    GetWanVpnInterfaceCellularAssociatedIpv6TrackerParcelsForTransportGetResponse,
)


class Ipv6TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        ipv6_tracker_id: str,
        payload: EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceCellular parcel and a IPv6 Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_tracker_id: Tracker ID
        :param payload: IPv6 Tracker Profile Parcel
        :returns: EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "ipv6-trackerId": ipv6_tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}",
            return_type=EditWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, cellular_id: str, ipv6_tracker_id: str, **kw):
        """
        Delete a WanVpnInterfaceCellular and a IPv6 Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "ipv6-trackerId": ipv6_tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        cellular_id: str,
        payload: CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceCellular parcel with a IPv6 Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/ipv6-tracker

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/ipv6-tracker",
            return_type=CreateWanVpnInterfaceCellularAndIpv6TrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, ipv6_tracker_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackerPayload:
        """
        Get WanVpnInterfaceCellular associated IPv6 Tracker Parcel by ipv6-trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, **kw
    ) -> List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceCellular associated IPv6 Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        ipv6_tracker_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str), (ipv6_tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
                "ipv6-trackerId": ipv6_tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker/{ipv6-trackerId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str)], [ipv6_tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-tracker",
                return_type=List[
                    GetWanVpnInterfaceCellularAssociatedIpv6TrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
