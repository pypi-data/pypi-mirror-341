# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNgfirewallFeaturePostRequest,
    CreateNgfirewallFeaturePostResponse,
    EditNgfirewallFeaturePutRequest,
    EditNgfirewallFeaturePutResponse,
    GetListSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
    GetSingleSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
)


class NgfirewallBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, security_id: str, payload: CreateNgfirewallFeaturePostRequest, **kw
    ) -> CreateNgfirewallFeaturePostResponse:
        """
        Create Parcel for Ngfirewall Policy
        POST /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall

        :param security_id: Feature Profile ID
        :param payload: Ngfirewall Feature
        :returns: CreateNgfirewallFeaturePostResponse
        """
        params = {
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall",
            return_type=CreateNgfirewallFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        security_id: str,
        security_profile_parcel_id: str,
        payload: EditNgfirewallFeaturePutRequest,
        **kw,
    ) -> EditNgfirewallFeaturePutResponse:
        """
        Update a Ngfirewall Feature
        PUT /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :param payload: Ngfirewall Feature
        :returns: EditNgfirewallFeaturePutResponse
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
            return_type=EditNgfirewallFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, security_id: str, security_profile_parcel_id: str, **kw):
        """
        Delete a Ngfirewall Feature
        DELETE /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :returns: None
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, security_id: str, security_profile_parcel_id: str, **kw
    ) -> GetSingleSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload:
        """
        Get Ngfirewall Feature by FeatureId
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :returns: GetSingleSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload
        """
        ...

    @overload
    def get(
        self, security_id: str, **kw
    ) -> GetListSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload:
        """
        Get Ngfirewall Feature
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall

        :param security_id: Feature Profile ID
        :returns: GetListSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload
        """
        ...

    def get(
        self, security_id: str, security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
        GetSingleSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}
        if self._request_adapter.param_checker(
            [(security_id, str), (security_profile_parcel_id, str)], []
        ):
            params = {
                "securityId": security_id,
                "securityProfileParcelId": security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
                return_type=GetSingleSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall
        if self._request_adapter.param_checker([(security_id, str)], [security_profile_parcel_id]):
            params = {
                "securityId": security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/unified/ngfirewall",
                return_type=GetListSdRoutingEmbeddedSecurityUnifiedNgfirewallPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
