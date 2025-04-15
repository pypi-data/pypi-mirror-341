# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse,
    GetDataPrefixProfileParcelForPolicyObjectGetResponse,
)


class ExpandedCommunityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectId}/expanded-community
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        payload: CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest,
        **kw,
    ) -> CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
        """
        Create a Data Prefix Profile Parcel for Security Policy Object feature profile
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/expanded-community

        :param policy_object_id: Feature Profile ID
        :param payload: Data Prefix Profile Parcel
        :returns: CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/expanded-community",
            return_type=CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, policy_object_id: str, parcel_id: str, reference_count: Optional[bool] = False, **kw
    ) -> GetDataPrefixProfileParcelForPolicyObjectGetResponse:
        """
        Get Data Prefix Profile Parcels for Policy Object feature profile
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/expanded-community/{parcelId}

        :param policy_object_id: Feature Profile ID
        :param reference_count: get reference count
        :param parcel_id: Parcel ID
        :returns: GetDataPrefixProfileParcelForPolicyObjectGetResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "referenceCount": reference_count,
            "parcelId": parcel_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/expanded-community/{parcelId}",
            return_type=GetDataPrefixProfileParcelForPolicyObjectGetResponse,
            params=params,
            **kw,
        )
