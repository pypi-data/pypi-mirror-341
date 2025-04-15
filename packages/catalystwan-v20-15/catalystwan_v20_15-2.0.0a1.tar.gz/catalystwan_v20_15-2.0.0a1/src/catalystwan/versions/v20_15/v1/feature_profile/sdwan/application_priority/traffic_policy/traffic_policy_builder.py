# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrafficPolicyProfileParcelForapplicationPriorityPostRequest,
    CreateTrafficPolicyProfileParcelForapplicationPriorityPostResponse,
    EditTrafficPolicyProfileParcelForapplicationPriorityPutRequest,
    EditTrafficPolicyProfileParcelForapplicationPriorityPutResponse,
    GetSingleSdwanApplicationPriorityTrafficPolicyPayload,
)


class TrafficPolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        application_priority_id: str,
        payload: CreateTrafficPolicyProfileParcelForapplicationPriorityPostRequest,
        **kw,
    ) -> CreateTrafficPolicyProfileParcelForapplicationPriorityPostResponse:
        """
        Create a Traffic Policy Profile Parcel for application-priority feature profile
        POST /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy

        :param application_priority_id: Feature Profile ID
        :param payload: Traffic Policy Profile Parcel
        :returns: CreateTrafficPolicyProfileParcelForapplicationPriorityPostResponse
        """
        params = {
            "applicationPriorityId": application_priority_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy",
            return_type=CreateTrafficPolicyProfileParcelForapplicationPriorityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, application_priority_id: str, traffic_policy_id: str, **kw
    ) -> GetSingleSdwanApplicationPriorityTrafficPolicyPayload:
        """
        Get Traffic Policy Profile Parcel by parcelId for application-priority feature profile
        GET /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}

        :param application_priority_id: Feature Profile ID
        :param traffic_policy_id: Profile Parcel ID
        :returns: GetSingleSdwanApplicationPriorityTrafficPolicyPayload
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "trafficPolicyId": traffic_policy_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}",
            return_type=GetSingleSdwanApplicationPriorityTrafficPolicyPayload,
            params=params,
            **kw,
        )

    def put(
        self,
        application_priority_id: str,
        traffic_policy_id: str,
        payload: EditTrafficPolicyProfileParcelForapplicationPriorityPutRequest,
        **kw,
    ) -> EditTrafficPolicyProfileParcelForapplicationPriorityPutResponse:
        """
        Update a Traffic Policy Profile Parcel for application-priority feature profile
        PUT /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}

        :param application_priority_id: Feature Profile ID
        :param traffic_policy_id: Profile Parcel ID
        :param payload: Traffic Policy Profile Parcel
        :returns: EditTrafficPolicyProfileParcelForapplicationPriorityPutResponse
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "trafficPolicyId": traffic_policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}",
            return_type=EditTrafficPolicyProfileParcelForapplicationPriorityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, application_priority_id: str, traffic_policy_id: str, **kw):
        """
        Delete a Traffic Policy Profile Parcel for application-priority feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}

        :param application_priority_id: Feature Profile ID
        :param traffic_policy_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "trafficPolicyId": traffic_policy_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/traffic-policy/{trafficPolicyId}",
            params=params,
            **kw,
        )
