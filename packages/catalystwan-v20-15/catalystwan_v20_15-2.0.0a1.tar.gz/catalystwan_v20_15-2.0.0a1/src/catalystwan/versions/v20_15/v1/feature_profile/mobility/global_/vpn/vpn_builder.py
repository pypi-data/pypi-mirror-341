# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateVpnProfileParcelForMobilityPostRequest,
    CreateVpnProfileParcelForMobilityPostResponse,
    EditVpnProfileParcelForMobilityPutRequest,
    EditVpnProfileParcelForMobilityPutResponse,
    GetListMobilityGlobalVpnPayload,
    GetSingleMobilityGlobalVpnPayload,
)


class VpnBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateVpnProfileParcelForMobilityPostRequest, **kw
    ) -> CreateVpnProfileParcelForMobilityPostResponse:
        """
        Create a VPN Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn

        :param profile_id: Feature Profile ID
        :param payload: VPN Profile Parcel
        :returns: CreateVpnProfileParcelForMobilityPostResponse
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/vpn",
            return_type=CreateVpnProfileParcelForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, profile_id: str, vpn_id: str, payload: EditVpnProfileParcelForMobilityPutRequest, **kw
    ) -> EditVpnProfileParcelForMobilityPutResponse:
        """
        Update a VPN Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}

        :param profile_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: VPN Profile Parcel
        :returns: EditVpnProfileParcelForMobilityPutResponse
        """
        params = {
            "profileId": profile_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}",
            return_type=EditVpnProfileParcelForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, vpn_id: str, **kw):
        """
        Delete a VPN Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}

        :param profile_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, profile_id: str, vpn_id: str, **kw) -> GetSingleMobilityGlobalVpnPayload:
        """
        Get VPN Profile Parcel by parcelId for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}

        :param profile_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalVpnPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalVpnPayload:
        """
        Get VPN Profile Parcels for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalVpnPayload
        """
        ...

    def get(
        self, profile_id: str, vpn_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalVpnPayload, GetSingleMobilityGlobalVpnPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}
        if self._request_adapter.param_checker([(profile_id, str), (vpn_id, str)], []):
            params = {
                "profileId": profile_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/vpn/{vpnId}",
                return_type=GetSingleMobilityGlobalVpnPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/vpn
        if self._request_adapter.param_checker([(profile_id, str)], [vpn_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/vpn",
                return_type=GetListMobilityGlobalVpnPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
