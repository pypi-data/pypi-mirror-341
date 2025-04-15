# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateServiceVrfAndRoutingOspfParcelAssociationPostRequest,
    CreateServiceVrfAndRoutingOspfParcelAssociationPostResponse,
    EditServiceVrfAndRoutingOspfFeatureAssociationPutRequest,
    EditServiceVrfAndRoutingOspfFeatureAssociationPutResponse,
    GetServiceVrfAssociatedRoutingOspfFeaturesGetResponse,
    GetSingleSdRoutingServiceVrfRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        payload: CreateServiceVrfAndRoutingOspfParcelAssociationPostRequest,
        **kw,
    ) -> CreateServiceVrfAndRoutingOspfParcelAssociationPostResponse:
        """
        Associate an OSPF feature with the LAN VRF feature for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: New OSPF Feature ID
        :returns: CreateServiceVrfAndRoutingOspfParcelAssociationPostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf",
            return_type=CreateServiceVrfAndRoutingOspfParcelAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        ospf_id: str,
        payload: EditServiceVrfAndRoutingOspfFeatureAssociationPutRequest,
        **kw,
    ) -> EditServiceVrfAndRoutingOspfFeatureAssociationPutResponse:
        """
        Replace the OSPF feature for LAN VRF feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospf_id: Old OSPF Feature ID
        :param payload: New OSPF Feature ID
        :returns: EditServiceVrfAndRoutingOspfFeatureAssociationPutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}",
            return_type=EditServiceVrfAndRoutingOspfFeatureAssociationPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, ospf_id: str, **kw):
        """
        Delete the LAN VRF feature and OSPF feature association in service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospf_id: OSPF Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, ospf_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfRoutingOspfPayload:
        """
        Get the LAN VRF associated OSPF feature by ID for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospf_id: OSPF Feature ID
        :returns: GetSingleSdRoutingServiceVrfRoutingOspfPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, **kw
    ) -> List[GetServiceVrfAssociatedRoutingOspfFeaturesGetResponse]:
        """
        Get the VRF associated OSPF features for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetServiceVrfAssociatedRoutingOspfFeaturesGetResponse]
        """
        ...

    def get(
        self, service_id: str, vrf_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetServiceVrfAssociatedRoutingOspfFeaturesGetResponse],
        GetSingleSdRoutingServiceVrfRoutingOspfPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ospf_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdRoutingServiceVrfRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [ospf_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospf",
                return_type=List[GetServiceVrfAssociatedRoutingOspfFeaturesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
