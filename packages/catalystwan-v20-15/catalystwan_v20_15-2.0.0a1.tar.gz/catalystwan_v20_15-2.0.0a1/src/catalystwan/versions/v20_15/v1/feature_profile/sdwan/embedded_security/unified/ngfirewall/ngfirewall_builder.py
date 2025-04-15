# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNgfirewallProfileParcelPostRequest,
    CreateNgfirewallProfileParcelPostResponse,
    EditNgfirewallProfileParcelPutRequest,
    EditNgfirewallProfileParcelPutResponse,
    GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
    GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
)


class NgfirewallBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, security_id: str, payload: CreateNgfirewallProfileParcelPostRequest, **kw
    ) -> CreateNgfirewallProfileParcelPostResponse:
        """
        Create Parcel for Ngfirewall Policy
        POST /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall

        :param security_id: Feature Profile ID
        :param payload: Ngfirewall Profile Parcel
        :returns: CreateNgfirewallProfileParcelPostResponse
        """
        params = {
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall",
            return_type=CreateNgfirewallProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        security_id: str,
        security_profile_parcel_id: str,
        payload: EditNgfirewallProfileParcelPutRequest,
        **kw,
    ) -> EditNgfirewallProfileParcelPutResponse:
        """
        Update a Ngfirewall Profile Parcel
        PUT /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Profile Parcel ID
        :param payload: Ngfirewall Profile Parcel
        :returns: EditNgfirewallProfileParcelPutResponse
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
            return_type=EditNgfirewallProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, security_id: str, security_profile_parcel_id: str, **kw):
        """
        Delete a Ngfirewall Profile Parcel
        DELETE /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

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
            "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, security_id: str, security_profile_parcel_id: str, **kw
    ) -> GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload:
        """
        Get Ngfirewall Profile Parcel by parcelId
        GET /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Profile Parcel ID
        :returns: GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload
        """
        ...

    @overload
    def get(self, security_id: str, **kw) -> GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload:
        """
        Get Ngfirewall Profile Parcel
        GET /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall

        :param security_id: Feature Profile ID
        :returns: GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload
        """
        ...

    def get(
        self, security_id: str, security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
        GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}
        if self._request_adapter.param_checker(
            [(security_id, str), (security_profile_parcel_id, str)], []
        ):
            params = {
                "securityId": security_id,
                "securityProfileParcelId": security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall/{securityProfileParcelId}",
                return_type=GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall
        if self._request_adapter.param_checker([(security_id, str)], [security_profile_parcel_id]):
            params = {
                "securityId": security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/embedded-security/{securityId}/unified/ngfirewall",
                return_type=GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
