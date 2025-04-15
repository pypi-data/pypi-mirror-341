# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfFeaturePostRequest,
    CreateSdroutingServiceVrfFeaturePostResponse,
    EditSdroutingServiceVrfFeaturePutRequest,
    EditSdroutingServiceVrfFeaturePutResponse,
    GetListSdRoutingServiceVrfPayload,
    GetSingleSdRoutingServiceVrfPayload,
)

if TYPE_CHECKING:
    from .dmvpn_tunnel.dmvpn_tunnel_builder import DmvpnTunnelBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .routing.routing_builder import RoutingBuilder


class VrfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfFeaturePostResponse:
        """
        Create a SD-Routing VRF Feature for Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf

        :param service_id: Service Profile ID
        :param payload:  VRF Feature for Service Feature Profile
        :returns: CreateSdroutingServiceVrfFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf",
            return_type=CreateSdroutingServiceVrfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, service_id: str, vrf_id: str, payload: EditSdroutingServiceVrfFeaturePutRequest, **kw
    ) -> EditSdroutingServiceVrfFeaturePutResponse:
        """
        Edit a SD-Routing VRF Feature for Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param payload:  VRF Feature for Service Feature Profile
        :returns: EditSdroutingServiceVrfFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}",
            return_type=EditSdroutingServiceVrfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, **kw):
        """
        Delete a SD-Routing VRF Feature for Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, vrf_id: str, **kw) -> GetSingleSdRoutingServiceVrfPayload:
        """
        Get a SD-Routing VRF Feature for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: GetSingleSdRoutingServiceVrfPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceVrfPayload:
        """
        Get all SD-Routing VRF Features for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceVrfPayload
        """
        ...

    def get(
        self, service_id: str, vrf_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingServiceVrfPayload, GetSingleSdRoutingServiceVrfPayload]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], []):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}",
                return_type=GetSingleSdRoutingServiceVrfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf
        if self._request_adapter.param_checker([(service_id, str)], [vrf_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf",
                return_type=GetListSdRoutingServiceVrfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def dmvpn_tunnel(self) -> DmvpnTunnelBuilder:
        """
        The dmvpn-tunnel property
        """
        from .dmvpn_tunnel.dmvpn_tunnel_builder import DmvpnTunnelBuilder

        return DmvpnTunnelBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)
