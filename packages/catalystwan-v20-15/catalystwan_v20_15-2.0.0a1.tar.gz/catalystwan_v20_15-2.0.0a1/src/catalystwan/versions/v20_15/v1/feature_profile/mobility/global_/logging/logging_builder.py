# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLoggingProfileFeatureForMobilityPostRequest,
    CreateLoggingProfileFeatureForMobilityPostResponse,
    EditLoggingProfileFeatureForMobilityPutRequest,
    EditLoggingProfileFeatureForMobilityPutResponse,
    GetListMobilityGlobalLoggingPayload,
    GetSingleMobilityGlobalLoggingPayload,
)


class LoggingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/logging
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateLoggingProfileFeatureForMobilityPostRequest, **kw
    ) -> CreateLoggingProfileFeatureForMobilityPostResponse:
        """
        Create a Logging Profile Feature for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/logging

        :param profile_id: Feature Profile ID
        :param payload: Logging Profile Feature
        :returns: CreateLoggingProfileFeatureForMobilityPostResponse
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/logging",
            return_type=CreateLoggingProfileFeatureForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        logging_id: str,
        payload: EditLoggingProfileFeatureForMobilityPutRequest,
        **kw,
    ) -> EditLoggingProfileFeatureForMobilityPutResponse:
        """
        Update a Logging Profile Feature for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}

        :param profile_id: Feature Profile ID
        :param logging_id: Profile Feature ID
        :param payload: Logging Profile Feature
        :returns: EditLoggingProfileFeatureForMobilityPutResponse
        """
        params = {
            "profileId": profile_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}",
            return_type=EditLoggingProfileFeatureForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, logging_id: str, **kw):
        """
        Delete a Logging Profile Feature for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}

        :param profile_id: Feature Profile ID
        :param logging_id: Profile Feature ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, profile_id: str, logging_id: str, **kw) -> GetSingleMobilityGlobalLoggingPayload:
        """
        Get Logging Profile Feature by parcelId for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}

        :param profile_id: Feature Profile ID
        :param logging_id: Profile Feature ID
        :returns: GetSingleMobilityGlobalLoggingPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalLoggingPayload:
        """
        Get Logging Profile Features for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/logging

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalLoggingPayload
        """
        ...

    def get(
        self, profile_id: str, logging_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalLoggingPayload, GetSingleMobilityGlobalLoggingPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}
        if self._request_adapter.param_checker([(profile_id, str), (logging_id, str)], []):
            params = {
                "profileId": profile_id,
                "loggingId": logging_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/logging/{loggingId}",
                return_type=GetSingleMobilityGlobalLoggingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/logging
        if self._request_adapter.param_checker([(profile_id, str)], [logging_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/logging",
                return_type=GetListMobilityGlobalLoggingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
