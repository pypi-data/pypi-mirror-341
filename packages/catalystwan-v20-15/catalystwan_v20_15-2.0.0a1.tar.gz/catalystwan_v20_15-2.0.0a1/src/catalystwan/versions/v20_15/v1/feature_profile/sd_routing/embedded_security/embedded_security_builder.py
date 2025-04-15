# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdRoutingEmbeddedSecurityFeatureProfilePostRequest,
    CreateSdRoutingEmbeddedSecurityFeatureProfilePostResponse,
    EditSdRoutingEmbeddedSecurityFeatureProfilePutRequest,
    EditSdRoutingEmbeddedSecurityFeatureProfilePutResponse,
    GetSdRoutingEmbeddedSecurityFeatureProfilesGetResponse,
    GetSingleSdRoutingEmbeddedSecurityPayload,
)

if TYPE_CHECKING:
    from .policy.policy_builder import PolicyBuilder
    from .unified.unified_builder import UnifiedBuilder


class EmbeddedSecurityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/embedded-security
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdRoutingEmbeddedSecurityFeatureProfilePostRequest, **kw
    ) -> CreateSdRoutingEmbeddedSecurityFeatureProfilePostResponse:
        """
        Create a SD-ROUTING Embedded Security Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/embedded-security

        :param payload: SD-ROUTING Feature profile
        :returns: CreateSdRoutingEmbeddedSecurityFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security",
            return_type=CreateSdRoutingEmbeddedSecurityFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self,
        embedded_security_id: str,
        payload: EditSdRoutingEmbeddedSecurityFeatureProfilePutRequest,
        **kw,
    ) -> EditSdRoutingEmbeddedSecurityFeatureProfilePutResponse:
        """
        Edit a SD-ROUTING Embedded Security Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}

        :param embedded_security_id: Feature Profile Id
        :param payload: SD-ROUTING Feature profile
        :returns: EditSdRoutingEmbeddedSecurityFeatureProfilePutResponse
        """
        params = {
            "embeddedSecurityId": embedded_security_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}",
            return_type=EditSdRoutingEmbeddedSecurityFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, embedded_security_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}

        :param embedded_security_id: Embedded security id
        :returns: None
        """
        params = {
            "embeddedSecurityId": embedded_security_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self,
        *,
        embedded_security_id: str,
        details: Optional[bool] = False,
        references: Optional[bool] = False,
        **kw,
    ) -> GetSingleSdRoutingEmbeddedSecurityPayload:
        """
        Get a SD-ROUTING Embedded Security Feature Profile with embeddedSecurityId
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}

        :param embedded_security_id: Feature Profile Id
        :param details: get feature details
        :param references: get associated group details
        :returns: GetSingleSdRoutingEmbeddedSecurityPayload
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
    ) -> List[GetSdRoutingEmbeddedSecurityFeatureProfilesGetResponse]:
        """
        Get all SD-ROUTING Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetSdRoutingEmbeddedSecurityFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        embedded_security_id: Optional[str] = None,
        details: Optional[bool] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[
        List[GetSdRoutingEmbeddedSecurityFeatureProfilesGetResponse],
        GetSingleSdRoutingEmbeddedSecurityPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}
        if self._request_adapter.param_checker(
            [(embedded_security_id, str)], [offset, limit, reference_count]
        ):
            params = {
                "embeddedSecurityId": embedded_security_id,
                "details": details,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security/{embeddedSecurityId}",
                return_type=GetSingleSdRoutingEmbeddedSecurityPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/embedded-security
        if self._request_adapter.param_checker([], [embedded_security_id, details, references]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security",
                return_type=List[GetSdRoutingEmbeddedSecurityFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)

    @property
    def unified(self) -> UnifiedBuilder:
        """
        The unified property
        """
        from .unified.unified_builder import UnifiedBuilder

        return UnifiedBuilder(self._request_adapter)
