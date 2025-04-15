# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEmbeddedSecurityProfileParcelPostRequest,
    CreateEmbeddedSecurityProfileParcelPostResponse,
    EditSecurityProfileParcelPutRequest,
    EditSecurityProfileParcelPutResponse,
    GetListSdwanEmbeddedSecurityPolicyPayload,
    GetSingleSdwanEmbeddedSecurityPolicyPayload,
)


class PolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/embedded-security/{securityId}/policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, security_id: str, payload: CreateEmbeddedSecurityProfileParcelPostRequest, **kw
    ) -> CreateEmbeddedSecurityProfileParcelPostResponse:
        """
        Create Parcel for Security Policy
        POST /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy

        :param security_id: Feature Profile ID
        :param payload: Security Profile Parcel
        :returns: CreateEmbeddedSecurityProfileParcelPostResponse
        """
        params = {
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy",
            return_type=CreateEmbeddedSecurityProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        security_id: str,
        security_profile_parcel_id: str,
        payload: EditSecurityProfileParcelPutRequest,
        **kw,
    ) -> EditSecurityProfileParcelPutResponse:
        """
        Update a Security Profile Parcel
        PUT /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Profile Parcel ID
        :param payload: Security Profile Parcel
        :returns: EditSecurityProfileParcelPutResponse
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}",
            return_type=EditSecurityProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, security_id: str, security_profile_parcel_id: str, **kw):
        """
        Delete a Security Profile Parcel
        DELETE /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, security_id: str, security_profile_parcel_id: str, **kw
    ) -> GetSingleSdwanEmbeddedSecurityPolicyPayload:
        """
        Get Security Profile Parcel by parcelId
        GET /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Profile Parcel ID
        :returns: GetSingleSdwanEmbeddedSecurityPolicyPayload
        """
        ...

    @overload
    def get(self, security_id: str, **kw) -> GetListSdwanEmbeddedSecurityPolicyPayload:
        """
        Get Security Profile Parcels for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy

        :param security_id: Feature Profile ID
        :returns: GetListSdwanEmbeddedSecurityPolicyPayload
        """
        ...

    def get(
        self, security_id: str, security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanEmbeddedSecurityPolicyPayload, GetSingleSdwanEmbeddedSecurityPolicyPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}
        if self._request_adapter.param_checker(
            [(security_id, str), (security_profile_parcel_id, str)], []
        ):
            params = {
                "securityId": security_id,
                "securityProfileParcelId": security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy/{securityProfileParcelId}",
                return_type=GetSingleSdwanEmbeddedSecurityPolicyPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy
        if self._request_adapter.param_checker([(security_id, str)], [security_profile_parcel_id]):
            params = {
                "securityId": security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/policy",
                return_type=GetListSdwanEmbeddedSecurityPolicyPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
