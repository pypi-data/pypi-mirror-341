# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateBasicProfileParcelForMobilityPostRequest,
    CreateBasicProfileParcelForMobilityPostResponse,
    EditBasicProfileParcelForMobilityPutRequest,
    EditBasicProfileParcelForMobilityPutResponse,
    GetListMobilityGlobalBasicPayload,
    GetSingleMobilityGlobalBasicPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BasicBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/basic
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateBasicProfileParcelForMobilityPostRequest, **kw
    ) -> CreateBasicProfileParcelForMobilityPostResponse:
        """
        Create a Basic Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/basic

        :param profile_id: Feature Profile ID
        :param payload: Basic Profile Parcel
        :returns: CreateBasicProfileParcelForMobilityPostResponse
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/basic",
            return_type=CreateBasicProfileParcelForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        parcel_id: str,
        payload: EditBasicProfileParcelForMobilityPutRequest,
        **kw,
    ) -> EditBasicProfileParcelForMobilityPutResponse:
        """
        Update a Basic Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}

        :param profile_id: Feature Profile ID
        :param parcel_id: Profile Parcel ID
        :param payload: Basic Profile Parcel
        :returns: EditBasicProfileParcelForMobilityPutResponse
        """
        params = {
            "profileId": profile_id,
            "parcelId": parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}",
            return_type=EditBasicProfileParcelForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, parcel_id: str, **kw):
        """
        Delete a Basic Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}

        :param profile_id: Feature Profile ID
        :param parcel_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "parcelId": parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, profile_id: str, parcel_id: str, **kw) -> GetSingleMobilityGlobalBasicPayload:
        """
        Get Basic Profile Parcel by parcelId for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}

        :param profile_id: Feature Profile ID
        :param parcel_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalBasicPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalBasicPayload:
        """
        Get Basic Profile Parcels for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/basic

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalBasicPayload
        """
        ...

    def get(
        self, profile_id: str, parcel_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalBasicPayload, GetSingleMobilityGlobalBasicPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}
        if self._request_adapter.param_checker([(profile_id, str), (parcel_id, str)], []):
            params = {
                "profileId": profile_id,
                "parcelId": parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/basic/{parcelId}",
                return_type=GetSingleMobilityGlobalBasicPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/basic
        if self._request_adapter.param_checker([(profile_id, str)], [parcel_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/basic",
                return_type=GetListMobilityGlobalBasicPayload,
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
