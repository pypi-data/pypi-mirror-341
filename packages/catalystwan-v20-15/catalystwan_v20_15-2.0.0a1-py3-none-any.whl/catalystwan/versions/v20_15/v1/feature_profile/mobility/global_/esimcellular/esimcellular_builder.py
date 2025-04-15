# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEsimCellularProfileFeatureForMobilityPostRequest,
    CreateEsimCellularProfileFeatureForMobilityPostResponse,
    EditEsimCellularProfileFeatureForMobilityPutRequest,
    EditEsimCellularProfileFeatureForMobilityPutResponse,
    GetListMobilityGlobalEsimcellularPayload,
    GetSingleMobilityGlobalEsimcellularPayload,
)


class EsimcellularBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/esimcellular
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateEsimCellularProfileFeatureForMobilityPostRequest, **kw
    ) -> CreateEsimCellularProfileFeatureForMobilityPostResponse:
        """
        Create a EsimCellular Profile Feature for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular

        :param profile_id: Feature Profile ID
        :param payload: EsimCellular Profile Feature
        :returns: CreateEsimCellularProfileFeatureForMobilityPostResponse
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular",
            return_type=CreateEsimCellularProfileFeatureForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        esim_cellular_id: str,
        payload: EditEsimCellularProfileFeatureForMobilityPutRequest,
        **kw,
    ) -> EditEsimCellularProfileFeatureForMobilityPutResponse:
        """
        Update a EsimCellular Profile Feature for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}

        :param profile_id: Feature Profile ID
        :param esim_cellular_id: Feature ID
        :param payload: EsimCellular Profile Feature
        :returns: EditEsimCellularProfileFeatureForMobilityPutResponse
        """
        params = {
            "profileId": profile_id,
            "esimCellularId": esim_cellular_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}",
            return_type=EditEsimCellularProfileFeatureForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, esim_cellular_id: str, **kw):
        """
        Delete a EsimCellular Profile Feature for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}

        :param profile_id: Feature Profile ID
        :param esim_cellular_id: Feature ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "esimCellularId": esim_cellular_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, profile_id: str, esim_cellular_id: str, **kw
    ) -> GetSingleMobilityGlobalEsimcellularPayload:
        """
        Get EsimCellular Profile Feature by Feature Id for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}

        :param profile_id: Feature Profile ID
        :param esim_cellular_id: Feature ID
        :returns: GetSingleMobilityGlobalEsimcellularPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalEsimcellularPayload:
        """
        Get EsimCellular Profile Features for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalEsimcellularPayload
        """
        ...

    def get(
        self, profile_id: str, esim_cellular_id: Optional[str] = None, **kw
    ) -> Union[
        GetListMobilityGlobalEsimcellularPayload, GetSingleMobilityGlobalEsimcellularPayload
    ]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}
        if self._request_adapter.param_checker([(profile_id, str), (esim_cellular_id, str)], []):
            params = {
                "profileId": profile_id,
                "esimCellularId": esim_cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular/{esimCellularId}",
                return_type=GetSingleMobilityGlobalEsimcellularPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular
        if self._request_adapter.param_checker([(profile_id, str)], [esim_cellular_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/esimcellular",
                return_type=GetListMobilityGlobalEsimcellularPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
