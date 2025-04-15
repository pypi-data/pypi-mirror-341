# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostRequest,
    CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostResponse,
    EditSdroutingServiceVrfOspfv3Ipv4FeaturePutRequest,
    EditSdroutingServiceVrfOspfv3Ipv4FeaturePutResponse,
    GetListSdRoutingServiceRoutingOspfv3Ipv4Payload,
    GetSingleSdRoutingServiceRoutingOspfv3Ipv4Payload,
)


class Ipv4Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostResponse:
        """
        Create a SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4

        :param service_id: Service Profile ID
        :param payload: SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        :returns: CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4",
            return_type=CreateSdroutingServiceVrfOspfv3Ipv4FeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospfv3_id: str,
        payload: EditSdroutingServiceVrfOspfv3Ipv4FeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfOspfv3Ipv4FeaturePutResponse:
        """
        Edit a SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :param payload: SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        :returns: EditSdroutingServiceVrfOspfv3Ipv4FeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
            return_type=EditSdroutingServiceVrfOspfv3Ipv4FeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospfv3_id: str, **kw):
        """
        Delete a SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingServiceRoutingOspfv3Ipv4Payload:
        """
        Get a SD-Routing LAN OSPFv3 IPv4 Feature for service VRF in Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :returns: GetSingleSdRoutingServiceRoutingOspfv3Ipv4Payload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceRoutingOspfv3Ipv4Payload:
        """
        Get all SD-Routing LAN OSPFv3 IPv4 Features for service VRF in Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceRoutingOspfv3Ipv4Payload
        """
        ...

    def get(
        self, service_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceRoutingOspfv3Ipv4Payload,
        GetSingleSdRoutingServiceRoutingOspfv3Ipv4Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}
        if self._request_adapter.param_checker([(service_id, str), (ospfv3_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
                return_type=GetSingleSdRoutingServiceRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4
        if self._request_adapter.param_checker([(service_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv4",
                return_type=GetListSdRoutingServiceRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
