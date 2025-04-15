# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSecurityPolicyProfileParcelForMobilityPostRequest,
    EditSecurityPolicyProfileParcelForMobilityPutRequest,
    GetListMobilityGlobalSecuritypolicyPayload,
    GetSingleMobilityGlobalSecuritypolicyPayload,
)


class SecurityPolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/securityPolicy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        profile_id: str,
        payload: CreateSecurityPolicyProfileParcelForMobilityPostRequest,
        **kw,
    ) -> str:
        """
        Create an SecurityPolicy Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy

        :param profile_id: Feature Profile ID
        :param payload: SecurityPolicy Profile Parcel
        :returns: str
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        security_policy_id: str,
        payload: EditSecurityPolicyProfileParcelForMobilityPutRequest,
        **kw,
    ):
        """
        Edit an Security Policy Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}

        :param profile_id: Feature Profile ID
        :param security_policy_id: Profile Parcel ID
        :param payload: Security Policy Profile Parcel
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "securityPolicyId": security_policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, security_policy_id: str, **kw):
        """
        Delete a Security Policy Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}

        :param profile_id: Feature Profile ID
        :param security_policy_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "securityPolicyId": security_policy_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, profile_id: str, security_policy_id: str, **kw
    ) -> GetSingleMobilityGlobalSecuritypolicyPayload:
        """
        Get an Mobility SecurityPolicy Profile Parcel for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}

        :param profile_id: Feature Profile ID
        :param security_policy_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalSecuritypolicyPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalSecuritypolicyPayload:
        """
        Get an Mobility SecurityPolicy Profile Parcel list for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalSecuritypolicyPayload
        """
        ...

    def get(
        self, profile_id: str, security_policy_id: Optional[str] = None, **kw
    ) -> Union[
        GetListMobilityGlobalSecuritypolicyPayload, GetSingleMobilityGlobalSecuritypolicyPayload
    ]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}
        if self._request_adapter.param_checker([(profile_id, str), (security_policy_id, str)], []):
            params = {
                "profileId": profile_id,
                "securityPolicyId": security_policy_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy/{securityPolicyId}",
                return_type=GetSingleMobilityGlobalSecuritypolicyPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy
        if self._request_adapter.param_checker([(profile_id, str)], [security_policy_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/securityPolicy",
                return_type=GetListMobilityGlobalSecuritypolicyPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
