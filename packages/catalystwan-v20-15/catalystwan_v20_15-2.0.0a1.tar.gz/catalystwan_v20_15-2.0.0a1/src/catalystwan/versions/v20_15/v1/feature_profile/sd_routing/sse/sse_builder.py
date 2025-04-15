# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdRoutingSseFeatureProfilePostRequest,
    CreateSdRoutingSseFeatureProfilePostResponse,
    EditSdRoutingSseFeatureProfilePutRequest,
    EditSdRoutingSseFeatureProfilePutResponse,
    GetSdRoutingSseFeatureProfilesGetResponse,
    GetSingleSdRoutingSsePayload,
)

if TYPE_CHECKING:
    from .cisco.cisco_builder import CiscoBuilder


class SseBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/sse
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdRoutingSseFeatureProfilePostRequest, **kw
    ) -> CreateSdRoutingSseFeatureProfilePostResponse:
        """
        Create a SD-ROUTING SSE Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/sse

        :param payload: SD-ROUTING Feature profile
        :returns: CreateSdRoutingSseFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/sse",
            return_type=CreateSdRoutingSseFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, sse_id: str, payload: EditSdRoutingSseFeatureProfilePutRequest, **kw
    ) -> EditSdRoutingSseFeatureProfilePutResponse:
        """
        Edit a SD-ROUTING SSE Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/sse/{sseId}

        :param sse_id: Feature Profile Id
        :param payload: SD-ROUTING Feature profile
        :returns: EditSdRoutingSseFeatureProfilePutResponse
        """
        params = {
            "sseId": sse_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}",
            return_type=EditSdRoutingSseFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, sse_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/sse/{sseId}

        :param sse_id: Sse id
        :returns: None
        """
        params = {
            "sseId": sse_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}", params=params, **kw
        )

    @overload
    def get(
        self, *, sse_id: str, references: Optional[bool] = False, **kw
    ) -> GetSingleSdRoutingSsePayload:
        """
        Get a SD-ROUTING SSE Feature Profile with sseId
        GET /dataservice/v1/feature-profile/sd-routing/sse/{sseId}

        :param sse_id: Feature Profile Id
        :param references: get associated group details
        :returns: GetSingleSdRoutingSsePayload
        """
        ...

    @overload
    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> List[GetSdRoutingSseFeatureProfilesGetResponse]:
        """
        Get all SD-ROUTING Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sd-routing/sse

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetSdRoutingSseFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        sse_id: Optional[str] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[List[GetSdRoutingSseFeatureProfilesGetResponse], GetSingleSdRoutingSsePayload]:
        # /dataservice/v1/feature-profile/sd-routing/sse/{sseId}
        if self._request_adapter.param_checker([(sse_id, str)], [offset, limit, reference_count]):
            params = {
                "sseId": sse_id,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/sse/{sseId}",
                return_type=GetSingleSdRoutingSsePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/sse
        if self._request_adapter.param_checker([], [sse_id, references]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/sse",
                return_type=List[GetSdRoutingSseFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def cisco(self) -> CiscoBuilder:
        """
        The cisco property
        """
        from .cisco.cisco_builder import CiscoBuilder

        return CiscoBuilder(self._request_adapter)
