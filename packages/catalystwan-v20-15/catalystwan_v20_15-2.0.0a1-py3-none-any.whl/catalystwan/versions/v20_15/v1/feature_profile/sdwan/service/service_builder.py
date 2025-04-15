# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanServiceFeatureProfilePostRequest,
    CreateSdwanServiceFeatureProfilePostResponse,
    EditSdwanServiceFeatureProfilePutRequest,
    EditSdwanServiceFeatureProfilePutResponse,
    GetSdwanServiceFeatureProfilesGetResponse,
    GetSingleSdwanServicePayload,
)

if TYPE_CHECKING:
    from .appqoe.appqoe_builder import AppqoeBuilder
    from .dhcp_server.dhcp_server_builder import DhcpServerBuilder
    from .lan.lan_builder import LanBuilder
    from .routing.routing_builder import RoutingBuilder
    from .switchport.switchport_builder import SwitchportBuilder
    from .tracker.tracker_builder import TrackerBuilder
    from .trackergroup.trackergroup_builder import TrackergroupBuilder
    from .wirelesslan.wirelesslan_builder import WirelesslanBuilder


class ServiceBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanServiceFeatureProfilePostRequest, **kw
    ) -> CreateSdwanServiceFeatureProfilePostResponse:
        """
        Create a SDWAN Service Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/service

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanServiceFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service",
            return_type=CreateSdwanServiceFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, service_id: str, payload: EditSdwanServiceFeatureProfilePutRequest, **kw
    ) -> EditSdwanServiceFeatureProfilePutResponse:
        """
        Edit a SDWAN Service Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}

        :param service_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanServiceFeatureProfilePutResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}",
            return_type=EditSdwanServiceFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}

        :param service_id: Service id
        :returns: None
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, *, service_id: str, details: Optional[bool] = False, **kw
    ) -> GetSingleSdwanServicePayload:
        """
        Get a SDWAN Service Feature Profile with serviceId
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}

        :param service_id: Feature Profile Id
        :param details: get feature details
        :returns: GetSingleSdwanServicePayload
        """
        ...

    @overload
    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        details: Optional[bool] = False,
        **kw,
    ) -> List[GetSdwanServiceFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/service

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param details: get configuration details
        :returns: List[GetSdwanServiceFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        details: Optional[bool] = None,
        service_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdwanServiceFeatureProfilesGetResponse], GetSingleSdwanServicePayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}
        if self._request_adapter.param_checker([(service_id, str)], [offset, limit]):
            params = {
                "serviceId": service_id,
                "details": details,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}",
                return_type=GetSingleSdwanServicePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service
        if self._request_adapter.param_checker([], [service_id]):
            params = {
                "offset": offset,
                "limit": limit,
                "details": details,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service",
                return_type=List[GetSdwanServiceFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def appqoe(self) -> AppqoeBuilder:
        """
        The appqoe property
        """
        from .appqoe.appqoe_builder import AppqoeBuilder

        return AppqoeBuilder(self._request_adapter)

    @property
    def dhcp_server(self) -> DhcpServerBuilder:
        """
        The dhcp-server property
        """
        from .dhcp_server.dhcp_server_builder import DhcpServerBuilder

        return DhcpServerBuilder(self._request_adapter)

    @property
    def lan(self) -> LanBuilder:
        """
        The lan property
        """
        from .lan.lan_builder import LanBuilder

        return LanBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)

    @property
    def switchport(self) -> SwitchportBuilder:
        """
        The switchport property
        """
        from .switchport.switchport_builder import SwitchportBuilder

        return SwitchportBuilder(self._request_adapter)

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)

    @property
    def trackergroup(self) -> TrackergroupBuilder:
        """
        The trackergroup property
        """
        from .trackergroup.trackergroup_builder import TrackergroupBuilder

        return TrackergroupBuilder(self._request_adapter)

    @property
    def wirelesslan(self) -> WirelesslanBuilder:
        """
        The wirelesslan property
        """
        from .wirelesslan.wirelesslan_builder import WirelesslanBuilder

        return WirelesslanBuilder(self._request_adapter)
