# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateAaaServersProfileParcelForMobilityPostRequest,
    CreateAaaServersProfileParcelForMobilityPostResponse,
    EditAaaServersProfileParcelForMobilityPutRequest,
    EditAaaServersProfileParcelForMobilityPutResponse,
    GetListMobilityGlobalAaaserversPayload,
    GetSingleMobilityGlobalAaaserversPayload,
)


class AaaserversBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/aaaservers
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateAaaServersProfileParcelForMobilityPostRequest, **kw
    ) -> CreateAaaServersProfileParcelForMobilityPostResponse:
        """
        Create a aaaservers Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers

        :param profile_id: Feature Profile ID
        :param payload: aaaservers Profile Parcel
        :returns: CreateAaaServersProfileParcelForMobilityPostResponse
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers",
            return_type=CreateAaaServersProfileParcelForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        aaaservers_id: str,
        payload: EditAaaServersProfileParcelForMobilityPutRequest,
        **kw,
    ) -> EditAaaServersProfileParcelForMobilityPutResponse:
        """
        Update a aaaservers Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}

        :param profile_id: Feature Profile ID
        :param aaaservers_id: Profile Parcel ID
        :param payload: aaaservers Profile Parcel
        :returns: EditAaaServersProfileParcelForMobilityPutResponse
        """
        params = {
            "profileId": profile_id,
            "aaaserversId": aaaservers_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}",
            return_type=EditAaaServersProfileParcelForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, aaaservers_id: str, **kw):
        """
        Delete a aaaservers Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}

        :param profile_id: Feature Profile ID
        :param aaaservers_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "aaaserversId": aaaservers_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, profile_id: str, aaaservers_id: str, **kw
    ) -> GetSingleMobilityGlobalAaaserversPayload:
        """
        Get aaaservers Profile Parcel by parcelId for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}

        :param profile_id: Feature Profile ID
        :param aaaservers_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalAaaserversPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalAaaserversPayload:
        """
        Get aaaservers Profile Parcels for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalAaaserversPayload
        """
        ...

    def get(
        self, profile_id: str, aaaservers_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalAaaserversPayload, GetSingleMobilityGlobalAaaserversPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}
        if self._request_adapter.param_checker([(profile_id, str), (aaaservers_id, str)], []):
            params = {
                "profileId": profile_id,
                "aaaserversId": aaaservers_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers/{aaaserversId}",
                return_type=GetSingleMobilityGlobalAaaserversPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers
        if self._request_adapter.param_checker([(profile_id, str)], [aaaservers_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/aaaservers",
                return_type=GetListMobilityGlobalAaaserversPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
