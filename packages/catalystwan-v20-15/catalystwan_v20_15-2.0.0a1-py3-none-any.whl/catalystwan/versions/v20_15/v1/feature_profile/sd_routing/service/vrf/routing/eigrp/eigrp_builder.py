# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfEigrpFeaturePostRequest,
    CreateSdroutingServiceVrfEigrpFeaturePostResponse,
    CreateServiceVrfAndRoutingEigrpFeatureAssociationPostRequest,
    CreateServiceVrfAndRoutingEigrpFeatureAssociationPostResponse,
    EditSdroutingServiceVrfEigrpFeaturePutRequest,
    EditSdroutingServiceVrfEigrpFeaturePutResponse,
    EditServiceVrfAndRoutingEigrpFeatureAssociationPutRequest,
    EditServiceVrfAndRoutingEigrpFeatureAssociationPutResponse,
    GetListSdRoutingServiceVrfRoutingEigrpPayload,
    GetServiceVrfAssociatedRoutingEigrpFeaturesGetResponse,
    GetSingleSdRoutingServiceVrfRoutingEigrpPayload,
    GetSingleSdRoutingServiceVrfVrfRoutingEigrpPayload,
)


class EigrpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(
        self, *, service_id: str, vrf_id: str, eigrp_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfVrfRoutingEigrpPayload:
        """
        Get the LAN VRF associated EIGRP feature by ID for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param eigrp_id: EIGRP Feature ID
        :returns: GetSingleSdRoutingServiceVrfVrfRoutingEigrpPayload
        """
        ...

    @overload
    def get(
        self, *, service_id: str, eigrp_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfRoutingEigrpPayload:
        """
        Get a SD-Routing VRF EIGRP Feature for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param eigrp_id: EIGRP Feature ID
        :returns: GetSingleSdRoutingServiceVrfRoutingEigrpPayload
        """
        ...

    @overload
    def get(
        self, *, service_id: str, vrf_id: str, **kw
    ) -> List[GetServiceVrfAssociatedRoutingEigrpFeaturesGetResponse]:
        """
        Get the LAN VRF associated EIGRP Features for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetServiceVrfAssociatedRoutingEigrpFeaturesGetResponse]
        """
        ...

    @overload
    def get(self, *, service_id: str, **kw) -> GetListSdRoutingServiceVrfRoutingEigrpPayload:
        """
        Get all SD-Routing VRF EIGRP Features for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceVrfRoutingEigrpPayload
        """
        ...

    def get(
        self, *, service_id: str, eigrp_id: Optional[str] = None, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfRoutingEigrpPayload,
        GetSingleSdRoutingServiceVrfRoutingEigrpPayload,
        List[GetServiceVrfAssociatedRoutingEigrpFeaturesGetResponse],
        GetSingleSdRoutingServiceVrfVrfRoutingEigrpPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (eigrp_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}",
                return_type=GetSingleSdRoutingServiceVrfVrfRoutingEigrpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker([(service_id, str), (eigrp_id, str)], [vrf_id]):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}",
                return_type=GetSingleSdRoutingServiceVrfRoutingEigrpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [eigrp_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp",
                return_type=List[GetServiceVrfAssociatedRoutingEigrpFeaturesGetResponse],
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp
        if self._request_adapter.param_checker([(service_id, str)], [eigrp_id, vrf_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp",
                return_type=GetListSdRoutingServiceVrfRoutingEigrpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def post(
        self,
        service_id: str,
        payload: CreateServiceVrfAndRoutingEigrpFeatureAssociationPostRequest,
        vrf_id: str,
        **kw,
    ) -> CreateServiceVrfAndRoutingEigrpFeatureAssociationPostResponse:
        """
        Associate a EIGRP feature with the LAN VRF feature for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp

        :param service_id: Service Profile ID
        :param payload: New EIGRP feature ID
        :param vrf_id: VRF Feature ID
        :returns: CreateServiceVrfAndRoutingEigrpFeatureAssociationPostResponse
        """
        ...

    @overload
    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfEigrpFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfEigrpFeaturePostResponse:
        """
        Create a SD-Routing VRF EIGRP Feature for Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp

        :param service_id: Service Profile ID
        :param payload: SD-Routing VRF EIGRP Feature for Service Feature Profile
        :returns: CreateSdroutingServiceVrfEigrpFeaturePostResponse
        """
        ...

    def post(
        self,
        service_id: str,
        payload: Union[
            CreateServiceVrfAndRoutingEigrpFeatureAssociationPostRequest,
            CreateSdroutingServiceVrfEigrpFeaturePostRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        CreateSdroutingServiceVrfEigrpFeaturePostResponse,
        CreateServiceVrfAndRoutingEigrpFeatureAssociationPostResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (payload, CreateServiceVrfAndRoutingEigrpFeatureAssociationPostRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp",
                return_type=CreateServiceVrfAndRoutingEigrpFeatureAssociationPostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp
        if self._request_adapter.param_checker(
            [(service_id, str), (payload, CreateSdroutingServiceVrfEigrpFeaturePostRequest)],
            [vrf_id],
        ):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp",
                return_type=CreateSdroutingServiceVrfEigrpFeaturePostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(
        self,
        service_id: str,
        eigrp_id: str,
        payload: EditServiceVrfAndRoutingEigrpFeatureAssociationPutRequest,
        vrf_id: str,
        **kw,
    ) -> EditServiceVrfAndRoutingEigrpFeatureAssociationPutResponse:
        """
        Replace the EIGRP feature for LAN VRF feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param eigrp_id: Old EIGRP Feature ID
        :param payload: New EIGRP feature ID
        :param vrf_id: VRF Feature ID
        :returns: EditServiceVrfAndRoutingEigrpFeatureAssociationPutResponse
        """
        ...

    @overload
    def put(
        self,
        service_id: str,
        eigrp_id: str,
        payload: EditSdroutingServiceVrfEigrpFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfEigrpFeaturePutResponse:
        """
        Edit a SD-Routing VRF EIGRP Feature for Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param eigrp_id: EIGRP Feature ID
        :param payload: SD-Routing VRF EIGRP Feature for Service Feature Profile
        :returns: EditSdroutingServiceVrfEigrpFeaturePutResponse
        """
        ...

    def put(
        self,
        service_id: str,
        eigrp_id: str,
        payload: Union[
            EditSdroutingServiceVrfEigrpFeaturePutRequest,
            EditServiceVrfAndRoutingEigrpFeatureAssociationPutRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        EditSdroutingServiceVrfEigrpFeaturePutResponse,
        EditServiceVrfAndRoutingEigrpFeatureAssociationPutResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (eigrp_id, str),
                (payload, EditServiceVrfAndRoutingEigrpFeatureAssociationPutRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}",
                return_type=EditServiceVrfAndRoutingEigrpFeatureAssociationPutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (eigrp_id, str),
                (payload, EditSdroutingServiceVrfEigrpFeaturePutRequest),
            ],
            [vrf_id],
        ):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}",
                return_type=EditSdroutingServiceVrfEigrpFeaturePutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def delete(self, service_id: str, eigrp_id: str, vrf_id: str, **kw):
        """
        Delete the LAN VRF feature and EIGRP feature association for service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param eigrp_id: EIGRP Feature ID
        :param vrf_id: VRF Feature ID
        :returns: None
        """
        ...

    @overload
    def delete(self, service_id: str, eigrp_id: str, **kw):
        """
        Delete a SD-Routing VRF EIGRP Feature for Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}

        :param service_id: Service Profile ID
        :param eigrp_id: EIGRP Feature ID
        :returns: None
        """
        ...

    def delete(self, service_id: str, eigrp_id: str, vrf_id: Optional[str] = None, **kw):
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (eigrp_id, str), (vrf_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/eigrp/{eigrpId}",
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker([(service_id, str), (eigrp_id, str)], [vrf_id]):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/eigrp/{eigrpId}",
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
