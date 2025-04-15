# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DisableCloudConnectorPutRequest, EnableCloudConnectorPostRequest

if TYPE_CHECKING:
    from .status.status_builder import StatusBuilder


class CloudconnectorBuilder:
    """
    Builds and executes requests for operations under /sdavc/cloudconnector
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get SD_AVC Cloud Connector Config
        GET /dataservice/sdavc/cloudconnector

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/sdavc/cloudconnector", **kw)

    def put(self, payload: DisableCloudConnectorPutRequest, **kw) -> Any:
        """
        Disable SD_AVC Cloud Connector
        PUT /dataservice/sdavc/cloudconnector

        :param payload: Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/sdavc/cloudconnector", payload=payload, **kw
        )

    def post(self, payload: EnableCloudConnectorPostRequest, **kw) -> Any:
        """
        Enable SD_AVC Cloud Connector
        POST /dataservice/sdavc/cloudconnector

        :param payload: Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sdavc/cloudconnector", payload=payload, **kw
        )

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
