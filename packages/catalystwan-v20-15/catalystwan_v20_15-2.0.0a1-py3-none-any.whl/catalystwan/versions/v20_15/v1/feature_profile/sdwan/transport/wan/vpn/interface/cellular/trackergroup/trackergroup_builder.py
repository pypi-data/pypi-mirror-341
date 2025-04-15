# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceCellularTrackergroupPayload,
    GetWanVpnInterfaceCellularAssociatedTrackerGroupParcelsForTransportGetResponse,
)


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        tracker_group_id: str,
        payload: EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceCellular parcel and a Tracker Group Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_group_id: Tracker Group ID
        :param payload: Tracker Group Profile Parcel
        :returns: EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "trackerGroupId": tracker_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}",
            return_type=EditWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, cellular_id: str, tracker_group_id: str, **kw):
        """
        Delete a WanVpnInterfaceCellular and a Tracker Group Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_group_id: Tracker Group Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "trackerGroupId": tracker_group_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        cellular_id: str,
        payload: CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceCellular parcel with a TrackerGroup Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel Id
        :returns: CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/trackergroup",
            return_type=CreateWanVpnInterfaceCellularAndTrackerGroupParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, tracker_group_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceCellularTrackergroupPayload:
        """
        Get WanVpnInterfaceCellular associated Tracker Group Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_group_id: Tracker Group Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceCellularTrackergroupPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, **kw
    ) -> List[GetWanVpnInterfaceCellularAssociatedTrackerGroupParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceCellular associated Tracker Group Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceCellularAssociatedTrackerGroupParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        tracker_group_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceCellularAssociatedTrackerGroupParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceCellularTrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str), (tracker_group_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
                "trackerGroupId": tracker_group_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup/{trackerGroupId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceCellularTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str)], [tracker_group_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/trackergroup",
                return_type=List[
                    GetWanVpnInterfaceCellularAssociatedTrackerGroupParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
