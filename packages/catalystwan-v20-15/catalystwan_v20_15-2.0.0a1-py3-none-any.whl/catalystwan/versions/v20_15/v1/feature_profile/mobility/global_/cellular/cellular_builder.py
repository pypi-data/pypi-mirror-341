# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CellularProfile,
    EditCellularProfileParcelForMobilityPutRequest,
    GetListMobilityGlobalCellularPayload,
    GetSingleMobilityGlobalCellularPayload,
)


class CellularBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/cellular
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, profile_id: str, payload: CellularProfile, **kw) -> str:
        """
        Create an cellular Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular

        :param profile_id: Feature Profile ID
        :param payload: Cellular Profile Parcel
        :returns: str
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/cellular",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        cellular_id: str,
        payload: EditCellularProfileParcelForMobilityPutRequest,
        **kw,
    ):
        """
        Edit an Cellular Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}

        :param profile_id: Feature Profile ID
        :param cellular_id: Profile Parcel ID
        :param payload: Cellular Profile Parcel
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, cellular_id: str, **kw):
        """
        Delete a Cellular Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}

        :param profile_id: Feature Profile ID
        :param cellular_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, profile_id: str, cellular_id: str, **kw
    ) -> GetSingleMobilityGlobalCellularPayload:
        """
        Get an Mobility Cellular Profile Parcel for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}

        :param profile_id: Feature Profile ID
        :param cellular_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalCellularPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalCellularPayload:
        """
        Get an Mobility Cellular Profile Parcel list for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalCellularPayload
        """
        ...

    def get(
        self, profile_id: str, cellular_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalCellularPayload, GetSingleMobilityGlobalCellularPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}
        if self._request_adapter.param_checker([(profile_id, str), (cellular_id, str)], []):
            params = {
                "profileId": profile_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/cellular/{cellularId}",
                return_type=GetSingleMobilityGlobalCellularPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/cellular
        if self._request_adapter.param_checker([(profile_id, str)], [cellular_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/cellular",
                return_type=GetListMobilityGlobalCellularPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
