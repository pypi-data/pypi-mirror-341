# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceRoutePolicyFeaturePostRequest,
    CreateSdroutingServiceRoutePolicyFeaturePostResponse,
    EditSdroutingServiceRoutePolicyFeaturePutRequest,
    EditSdroutingServiceRoutePolicyFeaturePutResponse,
    GetListSdRoutingServiceRoutePolicyPayload,
    GetSingleSdRoutingServiceRoutePolicyPayload,
)


class RoutePolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/route-policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceRoutePolicyFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceRoutePolicyFeaturePostResponse:
        """
        Create a SD-Routing Route Policy Feature for Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy

        :param service_id: Service Profile ID
        :param payload: SD-Routing Route Policy Feature for Service Feature Profile
        :returns: CreateSdroutingServiceRoutePolicyFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy",
            return_type=CreateSdroutingServiceRoutePolicyFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        route_policy_id: str,
        payload: EditSdroutingServiceRoutePolicyFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceRoutePolicyFeaturePutResponse:
        """
        Edit a SD-Routing Route Policy Feature for Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}

        :param service_id: Service Profile ID
        :param route_policy_id: Route Policy Feature ID
        :param payload: SD-Routing Route Policy Feature for Service Feature Profile
        :returns: EditSdroutingServiceRoutePolicyFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "routePolicyId": route_policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}",
            return_type=EditSdroutingServiceRoutePolicyFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, route_policy_id: str, **kw):
        """
        Delete a SD-Routing Route Policy Feature for Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}

        :param service_id: Service Profile ID
        :param route_policy_id: Route Policy Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "routePolicyId": route_policy_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, route_policy_id: str, **kw
    ) -> GetSingleSdRoutingServiceRoutePolicyPayload:
        """
        Get a SD-Routing Route Policy Feature for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}

        :param service_id: Service Profile ID
        :param route_policy_id: Route Policy Feature ID
        :returns: GetSingleSdRoutingServiceRoutePolicyPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceRoutePolicyPayload:
        """
        Get all SD-Routing Route Policy Features for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceRoutePolicyPayload
        """
        ...

    def get(
        self, service_id: str, route_policy_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceRoutePolicyPayload, GetSingleSdRoutingServiceRoutePolicyPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}
        if self._request_adapter.param_checker([(service_id, str), (route_policy_id, str)], []):
            params = {
                "serviceId": service_id,
                "routePolicyId": route_policy_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy/{routePolicyId}",
                return_type=GetSingleSdRoutingServiceRoutePolicyPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy
        if self._request_adapter.param_checker([(service_id, str)], [route_policy_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/route-policy",
                return_type=GetListSdRoutingServiceRoutePolicyPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
