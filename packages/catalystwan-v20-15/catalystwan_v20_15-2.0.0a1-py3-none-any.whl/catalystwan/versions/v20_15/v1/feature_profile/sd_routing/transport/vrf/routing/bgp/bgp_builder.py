# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportVrfBgpFeaturePostRequest,
    CreateSdroutingTransportVrfBgpFeaturePostResponse,
    CreateTransportVrfAndRoutingBgpFeatureAssociationPostRequest,
    CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse,
    EditSdroutingTransportVrfBgpFeaturePutRequest,
    EditSdroutingTransportVrfBgpFeaturePutResponse,
    EditTransportVrfAndRoutingBgpFeatureAssociationPutRequest,
    EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse,
    GetListSdRoutingTransportVrfRoutingBgpPayload,
    GetSingleSdRoutingTransportVrfRoutingBgpPayload,
    GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload,
    GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse,
)


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(
        self, *, transport_id: str, vrf_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload:
        """
        Get the WAN VRF associated BGP feature by BGP feature ID for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, transport_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfRoutingBgpPayload:
        """
        Get a SD-Routing WAN BGP feature for VRF in transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingTransportVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, transport_id: str, vrf_id: str, **kw
    ) -> List[GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse]:
        """
        Get the WAN VRF associated BGP features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse]
        """
        ...

    @overload
    def get(self, *, transport_id: str, **kw) -> GetListSdRoutingTransportVrfRoutingBgpPayload:
        """
        Get all SD-Routing WAN BGP features for VRF in transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportVrfRoutingBgpPayload
        """
        ...

    def get(
        self, *, transport_id: str, bgp_id: Optional[str] = None, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportVrfRoutingBgpPayload,
        GetSingleSdRoutingTransportVrfRoutingBgpPayload,
        List[GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse],
        GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (bgp_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(transport_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingTransportVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [bgp_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp",
                return_type=List[GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse],
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str)], [bgp_id, vrf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp",
                return_type=GetListSdRoutingTransportVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def post(
        self,
        transport_id: str,
        payload: CreateTransportVrfAndRoutingBgpFeatureAssociationPostRequest,
        vrf_id: str,
        **kw,
    ) -> CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse:
        """
        Associate a BGP feature with the WAN VRF feature for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp

        :param transport_id: Transport Profile ID
        :param payload: Routing BGP Profile feature Id
        :param vrf_id: VRF Feature ID
        :returns: CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse
        """
        ...

    @overload
    def post(
        self, transport_id: str, payload: CreateSdroutingTransportVrfBgpFeaturePostRequest, **kw
    ) -> CreateSdroutingTransportVrfBgpFeaturePostResponse:
        """
        Create a SD-Routing WAN BGP feature for VRF in transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing WAN BGP feature for VRF in transport feature profile
        :returns: CreateSdroutingTransportVrfBgpFeaturePostResponse
        """
        ...

    def post(
        self,
        transport_id: str,
        payload: Union[
            CreateTransportVrfAndRoutingBgpFeatureAssociationPostRequest,
            CreateSdroutingTransportVrfBgpFeaturePostRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        CreateSdroutingTransportVrfBgpFeaturePostResponse,
        CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (payload, CreateTransportVrfAndRoutingBgpFeatureAssociationPostRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp",
                return_type=CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp
        if self._request_adapter.param_checker(
            [(transport_id, str), (payload, CreateSdroutingTransportVrfBgpFeaturePostRequest)],
            [vrf_id],
        ):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp",
                return_type=CreateSdroutingTransportVrfBgpFeaturePostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: EditTransportVrfAndRoutingBgpFeatureAssociationPutRequest,
        vrf_id: str,
        **kw,
    ) -> EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse:
        """
        Replace the BGP feature for the WAN VRF feature in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: Old BGP Feature ID
        :param payload: New BGP feature ID
        :param vrf_id: VRF Feature ID
        :returns: EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse
        """
        ...

    @overload
    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: EditSdroutingTransportVrfBgpFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportVrfBgpFeaturePutResponse:
        """
        Edit a SD-Routing WAN BGP feature for VRF in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :param payload: SD-Routing WAN BGP feature for VRF in transport feature profile
        :returns: EditSdroutingTransportVrfBgpFeaturePutResponse
        """
        ...

    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: Union[
            EditSdroutingTransportVrfBgpFeaturePutRequest,
            EditTransportVrfAndRoutingBgpFeatureAssociationPutRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        EditSdroutingTransportVrfBgpFeaturePutResponse,
        EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (bgp_id, str),
                (payload, EditTransportVrfAndRoutingBgpFeatureAssociationPutRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (bgp_id, str),
                (payload, EditSdroutingTransportVrfBgpFeaturePutRequest),
            ],
            [vrf_id],
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}",
                return_type=EditSdroutingTransportVrfBgpFeaturePutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def delete(self, transport_id: str, bgp_id: str, vrf_id: str, **kw):
        """
        Delete the WAN VRF and BGP association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :param vrf_id: VRF Feature ID
        :returns: None
        """
        ...

    @overload
    def delete(self, transport_id: str, bgp_id: str, **kw):
        """
        Delete a SD-Routing WAN BGP feature for VRF in transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :returns: None
        """
        ...

    def delete(self, transport_id: str, bgp_id: str, vrf_id: Optional[str] = None, **kw):
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (bgp_id, str), (vrf_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(transport_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
