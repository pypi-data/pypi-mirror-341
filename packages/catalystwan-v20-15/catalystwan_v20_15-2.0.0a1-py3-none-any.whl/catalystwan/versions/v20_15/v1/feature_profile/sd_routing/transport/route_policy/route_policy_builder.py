# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportRoutePolicyFeaturePostRequest,
    CreateSdroutingTransportRoutePolicyFeaturePostResponse,
    EditSdroutingTransportRoutePolicyFeaturePutRequest,
    EditSdroutingTransportRoutePolicyFeaturePutResponse,
    GetListSdRoutingTransportRoutePolicyPayload,
    GetSingleSdRoutingTransportRoutePolicyPayload,
)


class RoutePolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/route-policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportRoutePolicyFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportRoutePolicyFeaturePostResponse:
        """
        Create a SD-Routing Route Policy Feature for Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing Route Policy Feature for Transport Feature Profile
        :returns: CreateSdroutingTransportRoutePolicyFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy",
            return_type=CreateSdroutingTransportRoutePolicyFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        route_policy_id: str,
        payload: EditSdroutingTransportRoutePolicyFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportRoutePolicyFeaturePutResponse:
        """
        Edit a SD-Routing Route Policy Feature for Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}

        :param transport_id: Transport Profile ID
        :param route_policy_id: Route Policy Feature ID
        :param payload: SD-Routing Route Policy Feature for Transport Feature Profile
        :returns: EditSdroutingTransportRoutePolicyFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "routePolicyId": route_policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}",
            return_type=EditSdroutingTransportRoutePolicyFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, route_policy_id: str, **kw):
        """
        Delete a SD-Routing Route Policy Feature for Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}

        :param transport_id: Transport Profile ID
        :param route_policy_id: Route Policy Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "routePolicyId": route_policy_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, route_policy_id: str, **kw
    ) -> GetSingleSdRoutingTransportRoutePolicyPayload:
        """
        Get a SD-Routing Route Policy Feature for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}

        :param transport_id: Transport Profile ID
        :param route_policy_id: Route Policy Feature ID
        :returns: GetSingleSdRoutingTransportRoutePolicyPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportRoutePolicyPayload:
        """
        Get all SD-Routing Route Policy Features for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportRoutePolicyPayload
        """
        ...

    def get(
        self, transport_id: str, route_policy_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportRoutePolicyPayload, GetSingleSdRoutingTransportRoutePolicyPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}
        if self._request_adapter.param_checker([(transport_id, str), (route_policy_id, str)], []):
            params = {
                "transportId": transport_id,
                "routePolicyId": route_policy_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy/{routePolicyId}",
                return_type=GetSingleSdRoutingTransportRoutePolicyPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy
        if self._request_adapter.param_checker([(transport_id, str)], [route_policy_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/route-policy",
                return_type=GetListSdRoutingTransportRoutePolicyPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
