# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSecurityProfileParcelPostRequest1,
    CreateSecurityProfileParcelPostRequest2,
    CreateSecurityProfileParcelPostResponse,
    GetSecurityProfileParcelGetResponse,
)


class SslDecryptionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        payload: Union[
            CreateSecurityProfileParcelPostRequest1, CreateSecurityProfileParcelPostRequest2
        ],
        **kw,
    ) -> CreateSecurityProfileParcelPostResponse:
        """
        Create Parcel for Security Policy
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption

        :param policy_object_id: Feature Profile ID
        :param payload: Security Profile Parcel
        :returns: CreateSecurityProfileParcelPostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption",
            return_type=CreateSecurityProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, policy_object_id: str, parcel_id: str, reference_count: Optional[bool] = False, **kw
    ) -> GetSecurityProfileParcelGetResponse:
        """
        Get Security Profile Parcels for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption/{parcelId}

        :param policy_object_id: Feature Profile ID
        :param reference_count: get reference count
        :param parcel_id: Parcel ID
        :returns: GetSecurityProfileParcelGetResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "referenceCount": reference_count,
            "parcelId": parcel_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption/{parcelId}",
            return_type=GetSecurityProfileParcelGetResponse,
            params=params,
            **kw,
        )
