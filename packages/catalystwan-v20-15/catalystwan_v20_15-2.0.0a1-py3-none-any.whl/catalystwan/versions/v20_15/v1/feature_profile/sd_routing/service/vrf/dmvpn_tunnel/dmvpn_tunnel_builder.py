# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostRequest,
    CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostResponse,
    EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutRequest,
    EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutResponse,
    GetListSdRoutingServiceVrfLanDmvpnTunnelPayload,
    GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload,
)


class DmvpnTunnelBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        payload: CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostRequest,
        **kw,
    ) -> CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostResponse:
        """
        Create a SD-Routing VRF DMVPN Tunnel Feature for Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: SD-Routing VRF DMVPN Tunnel Feature Schema
        :returns: CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel",
            return_type=CreateSdroutingServiceVrfDmvpnTunnelFeatureForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        tunnel_id: str,
        payload: EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutResponse:
        """
        Edit a SD-Routing VRF DMVPN Tunnel Feature for Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param tunnel_id: DMVPN Tunnel Interface Feature ID
        :param payload: SD-Routing VRF DMVPN Tunnel Feature Schema
        :returns: EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "tunnelId": tunnel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}",
            return_type=EditSdroutingServiceVrfDmvpnTunnelFeatureForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, tunnel_id: str, **kw):
        """
        Delete a SD-Routing VRF DMVPN Tunnel Feature for Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param tunnel_id: DMVPN Tunnel Interface Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "tunnelId": tunnel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, tunnel_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload:
        """
        Get a SD-Routing VRF DMVPN Tunnel Feature by tunnelId for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param tunnel_id: DMVPN Tunnel Interface Feature ID
        :returns: GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingServiceVrfLanDmvpnTunnelPayload:
        """
        Get all  VRF DMVPN Tunnel Features for Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: GetListSdRoutingServiceVrfLanDmvpnTunnelPayload
        """
        ...

    def get(
        self, service_id: str, vrf_id: str, tunnel_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfLanDmvpnTunnelPayload,
        GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (tunnel_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "tunnelId": tunnel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel/{tunnelId}",
                return_type=GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [tunnel_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/dmvpn-tunnel",
                return_type=GetListSdRoutingServiceVrfLanDmvpnTunnelPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
