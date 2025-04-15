# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectDeviceLink, InterconnectTypeParam, ProcessResponse

if TYPE_CHECKING:
    from .metro_speed.metro_speed_builder import MetroSpeedBuilder
    from .port_speeds.port_speeds_builder import PortSpeedsBuilder


class DeviceLinksBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity/device-links
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_interconnect_device_links(
        self,
        device_link_name: Optional[str] = None,
        interconnect_type: Optional[InterconnectTypeParam] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> InterconnectDeviceLink:
        """
        API to retrieve Interconnect provider Device-Link.
        GET /dataservice/multicloud/interconnect/connectivity/device-links

        :param device_link_name: Interconnect Device Link name
        :param interconnect_type: Interconnect Provider Type
        :param refresh: Retrieve Interconnect Device-Link from provider enabled
        :returns: InterconnectDeviceLink
        """
        params = {
            "device-link-name": device_link_name,
            "interconnect-type": interconnect_type,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/device-links",
            return_type=InterconnectDeviceLink,
            params=params,
            **kw,
        )

    def post(self, payload: InterconnectDeviceLink, **kw) -> ProcessResponse:
        """
        API to create a Device-Link in vManage.
        POST /dataservice/multicloud/interconnect/connectivity/device-links

        :param payload: Request Payload for Multicloud Interconnect Device Links
        :returns: ProcessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/connectivity/device-links",
            return_type=ProcessResponse,
            payload=payload,
            **kw,
        )

    def get(self, device_link_name: str, **kw) -> InterconnectDeviceLink:
        """
        API to retrieve Interconnect provider Device-Link.
        GET /dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}

        :param device_link_name: Interconnect Device Link name
        :returns: InterconnectDeviceLink
        """
        params = {
            "device-link-name": device_link_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}",
            return_type=InterconnectDeviceLink,
            params=params,
            **kw,
        )

    def put(self, device_link_name: str, payload: InterconnectDeviceLink, **kw) -> ProcessResponse:
        """
        API to update a Device-Link in vManage.
        PUT /dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}

        :param device_link_name: Interconnect Device Link name
        :param payload: Request Payload for Multicloud Interconnect Device Links
        :returns: ProcessResponse
        """
        params = {
            "device-link-name": device_link_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}",
            return_type=ProcessResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, device_link_name: str, **kw):
        """
        API to Delete Interconnect provider Device-Link.
        DELETE /dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}

        :param device_link_name: Interconnect Device Link name
        :returns: None
        """
        params = {
            "device-link-name": device_link_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/connectivity/device-links/{device-link-name}",
            params=params,
            **kw,
        )

    @property
    def metro_speed(self) -> MetroSpeedBuilder:
        """
        The metro-speed property
        """
        from .metro_speed.metro_speed_builder import MetroSpeedBuilder

        return MetroSpeedBuilder(self._request_adapter)

    @property
    def port_speeds(self) -> PortSpeedsBuilder:
        """
        The port-speeds property
        """
        from .port_speeds.port_speeds_builder import PortSpeedsBuilder

        return PortSpeedsBuilder(self._request_adapter)
