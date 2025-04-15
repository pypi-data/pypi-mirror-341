# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportFeatureProfilePostRequest,
    CreateSdroutingTransportFeatureProfilePostResponse,
    EditSdroutingTransportFeatureProfilePutRequest,
    EditSdroutingTransportFeatureProfilePutResponse,
    GetSdroutingTransportFeatureProfilesGetResponse,
    GetSingleSdRoutingTransportPayload,
)

if TYPE_CHECKING:
    from .global_vrf.global_vrf_builder import GlobalVrfBuilder
    from .ipv4_acl.ipv4_acl_builder import Ipv4AclBuilder
    from .management_vrf.management_vrf_builder import ManagementVrfBuilder
    from .multicloud_connection.multicloud_connection_builder import MulticloudConnectionBuilder
    from .objecttracker.objecttracker_builder import ObjecttrackerBuilder
    from .objecttrackergroup.objecttrackergroup_builder import ObjecttrackergroupBuilder
    from .route_policy.route_policy_builder import RoutePolicyBuilder
    from .routing.routing_builder import RoutingBuilder
    from .vrf.vrf_builder import VrfBuilder


class TransportBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdroutingTransportFeatureProfilePostRequest, **kw
    ) -> CreateSdroutingTransportFeatureProfilePostResponse:
        """
        Create a SD-Routing Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport

        :param payload: SD-Routing Transport Feature Profile
        :returns: CreateSdroutingTransportFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport",
            return_type=CreateSdroutingTransportFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, transport_id: str, payload: EditSdroutingTransportFeatureProfilePutRequest, **kw
    ) -> EditSdroutingTransportFeatureProfilePutResponse:
        """
        Edit a SD-Routing Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}

        :param transport_id: Transport Profile Id
        :param payload: SD-Routing Transport Feature Profile
        :returns: EditSdroutingTransportFeatureProfilePutResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}",
            return_type=EditSdroutingTransportFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, **kw):
        """
        Delete a SD-Routing Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}

        :param transport_id: Transport Profile Id
        :returns: None
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, *, transport_id: str, **kw) -> GetSingleSdRoutingTransportPayload:
        """
        Get a SD-Routing Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}

        :param transport_id: Transport Profile Id
        :returns: GetSingleSdRoutingTransportPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdroutingTransportFeatureProfilesGetResponse]:
        """
        Get all SD-Routing Transport Feature Profiles
        GET /dataservice/v1/feature-profile/sd-routing/transport

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdroutingTransportFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        transport_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetSdroutingTransportFeatureProfilesGetResponse], GetSingleSdRoutingTransportPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}
        if self._request_adapter.param_checker([(transport_id, str)], [offset, limit]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}",
                return_type=GetSingleSdRoutingTransportPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport
        if self._request_adapter.param_checker([], [transport_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport",
                return_type=List[GetSdroutingTransportFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def global_vrf(self) -> GlobalVrfBuilder:
        """
        The global-vrf property
        """
        from .global_vrf.global_vrf_builder import GlobalVrfBuilder

        return GlobalVrfBuilder(self._request_adapter)

    @property
    def ipv4_acl(self) -> Ipv4AclBuilder:
        """
        The ipv4-acl property
        """
        from .ipv4_acl.ipv4_acl_builder import Ipv4AclBuilder

        return Ipv4AclBuilder(self._request_adapter)

    @property
    def management_vrf(self) -> ManagementVrfBuilder:
        """
        The management-vrf property
        """
        from .management_vrf.management_vrf_builder import ManagementVrfBuilder

        return ManagementVrfBuilder(self._request_adapter)

    @property
    def multicloud_connection(self) -> MulticloudConnectionBuilder:
        """
        The multicloud-connection property
        """
        from .multicloud_connection.multicloud_connection_builder import MulticloudConnectionBuilder

        return MulticloudConnectionBuilder(self._request_adapter)

    @property
    def objecttracker(self) -> ObjecttrackerBuilder:
        """
        The objecttracker property
        """
        from .objecttracker.objecttracker_builder import ObjecttrackerBuilder

        return ObjecttrackerBuilder(self._request_adapter)

    @property
    def objecttrackergroup(self) -> ObjecttrackergroupBuilder:
        """
        The objecttrackergroup property
        """
        from .objecttrackergroup.objecttrackergroup_builder import ObjecttrackergroupBuilder

        return ObjecttrackergroupBuilder(self._request_adapter)

    @property
    def route_policy(self) -> RoutePolicyBuilder:
        """
        The route-policy property
        """
        from .route_policy.route_policy_builder import RoutePolicyBuilder

        return RoutePolicyBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)

    @property
    def vrf(self) -> VrfBuilder:
        """
        The vrf property
        """
        from .vrf.vrf_builder import VrfBuilder

        return VrfBuilder(self._request_adapter)
