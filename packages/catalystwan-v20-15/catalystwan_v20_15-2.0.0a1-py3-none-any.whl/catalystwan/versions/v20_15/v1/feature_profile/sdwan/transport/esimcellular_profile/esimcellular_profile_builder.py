# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEsimCellularProfileProfileFeatureForTransportPostRequest,
    CreateEsimCellularProfileProfileFeatureForTransportPostResponse,
    EditEsimCellularProfileProfileFeatureForTransportPutRequest,
    EditEsimCellularProfileProfileFeatureForTransportPutResponse,
    GetListSdwanTransportEsimcellularProfilePayload,
    GetSingleSdwanTransportEsimcellularProfilePayload,
)


class EsimcellularProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateEsimCellularProfileProfileFeatureForTransportPostRequest,
        **kw,
    ) -> CreateEsimCellularProfileProfileFeatureForTransportPostResponse:
        """
        Create a EsimCellular Profile Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile

        :param transport_id: Feature Profile ID
        :param payload: EsimCellular Profile Feature
        :returns: CreateEsimCellularProfileProfileFeatureForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile",
            return_type=CreateEsimCellularProfileProfileFeatureForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        esim_cellular_profile_id: str,
        payload: EditEsimCellularProfileProfileFeatureForTransportPutRequest,
        **kw,
    ) -> EditEsimCellularProfileProfileFeatureForTransportPutResponse:
        """
        Update a EsimCellular Profile Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_profile_id: Feature ID
        :param payload: EsimCellular Profile Feature
        :returns: EditEsimCellularProfileProfileFeatureForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "esimCellularProfileId": esim_cellular_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}",
            return_type=EditEsimCellularProfileProfileFeatureForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, esim_cellular_profile_id: str, **kw):
        """
        Delete a EsimCellular Profile Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_profile_id: Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "esimCellularProfileId": esim_cellular_profile_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, esim_cellular_profile_id: str, **kw
    ) -> GetSingleSdwanTransportEsimcellularProfilePayload:
        """
        Get EsimCellular Profile Feature by Feature Id for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_profile_id: Feature ID
        :returns: GetSingleSdwanTransportEsimcellularProfilePayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportEsimcellularProfilePayload:
        """
        Get EsimCellular Profile Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportEsimcellularProfilePayload
        """
        ...

    def get(
        self, transport_id: str, esim_cellular_profile_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportEsimcellularProfilePayload,
        GetSingleSdwanTransportEsimcellularProfilePayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (esim_cellular_profile_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "esimCellularProfileId": esim_cellular_profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile/{esimCellularProfileId}",
                return_type=GetSingleSdwanTransportEsimcellularProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile
        if self._request_adapter.param_checker([(transport_id, str)], [esim_cellular_profile_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-profile",
                return_type=GetListSdwanTransportEsimcellularProfilePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
