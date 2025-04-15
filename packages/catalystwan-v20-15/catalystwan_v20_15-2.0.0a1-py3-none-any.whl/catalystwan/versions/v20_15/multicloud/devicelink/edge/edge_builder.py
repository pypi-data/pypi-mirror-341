# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam

if TYPE_CHECKING:
    from .portspeed.portspeed_builder import PortspeedBuilder


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/devicelink/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        edge_type: Optional[EdgeTypeParam] = None,
        device_link_name: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Device Links
        GET /dataservice/multicloud/devicelink/edge

        :param edge_type: Edge type
        :param device_link_name: Device Link Name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getDeviceLinks")
        params = {
            "edgeType": edge_type,
            "deviceLinkName": device_link_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/devicelink/edge", params=params, **kw
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Update Device Link
        PUT /dataservice/multicloud/devicelink/edge

        :param payload: Device Link
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "updateDeviceLink")
        return self._request_adapter.request(
            "PUT", "/dataservice/multicloud/devicelink/edge", payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create Device Link
        POST /dataservice/multicloud/devicelink/edge

        :param payload: Device Link
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createDeviceLink")
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/devicelink/edge", payload=payload, **kw
        )

    def delete(self, device_link_name: str, **kw) -> Any:
        """
        Delete Device Link
        DELETE /dataservice/multicloud/devicelink/edge/{deviceLinkName}

        :param device_link_name: Device Link Name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "deleteDeviceLink")
        params = {
            "deviceLinkName": device_link_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/devicelink/edge/{deviceLinkName}",
            params=params,
            **kw,
        )

    @property
    def portspeed(self) -> PortspeedBuilder:
        """
        The portspeed property
        """
        from .portspeed.portspeed_builder import PortspeedBuilder

        return PortspeedBuilder(self._request_adapter)
