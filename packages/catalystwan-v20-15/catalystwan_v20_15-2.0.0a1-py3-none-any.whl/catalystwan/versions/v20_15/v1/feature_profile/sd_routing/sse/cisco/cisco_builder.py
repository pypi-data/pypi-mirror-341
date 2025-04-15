# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCiscoSseFeatureForSsePostRequest,
    CreateCiscoSseFeatureForSsePostResponse,
    EditCiscoSseFeaturePutRequest,
    EditCiscoSseFeaturePutResponse,
    GetListSdRoutingSseCiscoSsePayload,
    GetSingleSdRoutingSseCiscoSsePayload,
)


class CiscoBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/sse/{sseId}/cisco
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, sse_id: str, payload: CreateCiscoSseFeatureForSsePostRequest, **kw
    ) -> CreateCiscoSseFeatureForSsePostResponse:
        """
        Create Cisco Sse feature for sse feature profile type
        POST /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco

        :param sse_id: Feature Profile ID
        :param payload: Cisco Sse feature
        :returns: CreateCiscoSseFeatureForSsePostResponse
        """
        params = {
            "sseId": sse_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco",
            return_type=CreateCiscoSseFeatureForSsePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, sse_id: str, cisco_sse_id: str, payload: EditCiscoSseFeaturePutRequest, **kw
    ) -> EditCiscoSseFeaturePutResponse:
        """
        Update a Cisco Sse feature
        PUT /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}

        :param sse_id: Feature Profile ID
        :param cisco_sse_id: Feature ID
        :param payload: Cisco Sse feature
        :returns: EditCiscoSseFeaturePutResponse
        """
        params = {
            "sseId": sse_id,
            "ciscoSseId": cisco_sse_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}",
            return_type=EditCiscoSseFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, sse_id: str, cisco_sse_id: str, **kw):
        """
        Delete a Cisco Sse Feature
        DELETE /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}

        :param sse_id: Feature Profile ID
        :param cisco_sse_id: Feature ID
        :returns: None
        """
        params = {
            "sseId": sse_id,
            "ciscoSseId": cisco_sse_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, sse_id: str, cisco_sse_id: str, **kw) -> GetSingleSdRoutingSseCiscoSsePayload:
        """
        Get Cisco SSE Profile Feature by feature Id
        GET /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}

        :param sse_id: Feature Profile ID
        :param cisco_sse_id: Feature ID
        :returns: GetSingleSdRoutingSseCiscoSsePayload
        """
        ...

    @overload
    def get(self, sse_id: str, **kw) -> GetListSdRoutingSseCiscoSsePayload:
        """
        Get Cisco Sse feature list for Sse feature profile
        GET /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco

        :param sse_id: Feature Profile ID
        :returns: GetListSdRoutingSseCiscoSsePayload
        """
        ...

    def get(
        self, sse_id: str, cisco_sse_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingSseCiscoSsePayload, GetSingleSdRoutingSseCiscoSsePayload]:
        # /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}
        if self._request_adapter.param_checker([(sse_id, str), (cisco_sse_id, str)], []):
            params = {
                "sseId": sse_id,
                "ciscoSseId": cisco_sse_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco/{ciscoSseId}",
                return_type=GetSingleSdRoutingSseCiscoSsePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco
        if self._request_adapter.param_checker([(sse_id, str)], [cisco_sse_id]):
            params = {
                "sseId": sse_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}/cisco",
                return_type=GetListSdRoutingSseCiscoSsePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
