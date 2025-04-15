# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingDhcpServerProfileParcelPostRequest,
    CreateSdroutingDhcpServerProfileParcelPostResponse,
    EditSdroutingDhcpServerProfileParcelPutRequest,
    EditSdroutingDhcpServerProfileParcelPutResponse,
    GetListSdRoutingServiceDhcpServerPayload,
    GetSingleSdRoutingServiceDhcpServerPayload,
)


class DhcpServerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingDhcpServerProfileParcelPostRequest, **kw
    ) -> CreateSdroutingDhcpServerProfileParcelPostResponse:
        """
        Create a SD-Routing DHCP Server feature in service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server

        :param service_id: Service Profile ID
        :param payload: SD-Routing DHCP Server feature in service feature profile
        :returns: CreateSdroutingDhcpServerProfileParcelPostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server",
            return_type=CreateSdroutingDhcpServerProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        dhcp_server_id: str,
        payload: EditSdroutingDhcpServerProfileParcelPutRequest,
        **kw,
    ) -> EditSdroutingDhcpServerProfileParcelPutResponse:
        """
        Edit a SD-Routing DHCP Server feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param dhcp_server_id: DHCP Server Feature ID
        :param payload: SD-Routing DHCP Server feature in service feature profile
        :returns: EditSdroutingDhcpServerProfileParcelPutResponse
        """
        params = {
            "serviceId": service_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}",
            return_type=EditSdroutingDhcpServerProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, dhcp_server_id: str, **kw):
        """
        Delete a SD-Routing DHCP Server feature in service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param dhcp_server_id: DHCP Server Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, dhcp_server_id: str, **kw
    ) -> GetSingleSdRoutingServiceDhcpServerPayload:
        """
        Get a SD-Routing DHCP Server feature in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param dhcp_server_id: DHCP Server Feature ID
        :returns: GetSingleSdRoutingServiceDhcpServerPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceDhcpServerPayload:
        """
        Get all SD-Routing DHCP Server features in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceDhcpServerPayload
        """
        ...

    def get(
        self, service_id: str, dhcp_server_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceDhcpServerPayload, GetSingleSdRoutingServiceDhcpServerPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}
        if self._request_adapter.param_checker([(service_id, str), (dhcp_server_id, str)], []):
            params = {
                "serviceId": service_id,
                "dhcpServerId": dhcp_server_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server/{dhcpServerId}",
                return_type=GetSingleSdRoutingServiceDhcpServerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server
        if self._request_adapter.param_checker([(service_id, str)], [dhcp_server_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/dhcp-server",
                return_type=GetListSdRoutingServiceDhcpServerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
