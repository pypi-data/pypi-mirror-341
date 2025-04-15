# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ConnectedSitesResponse

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class ConnectedSitesBuilder:
    """
    Builds and executes requests for operations under /multicloud/connected-sites
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, cloud_type: str, cloud_gateway_name: Optional[str] = None, **kw
    ) -> ConnectedSitesResponse:
        """
        Get sites with connectivity to the cloud by cloud type
        GET /dataservice/multicloud/connected-sites/{cloudType}

        :param cloud_type: Cloud type
        :param cloud_gateway_name: Cloud gateway name
        :returns: ConnectedSitesResponse
        """
        params = {
            "cloudType": cloud_type,
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/connected-sites/{cloudType}",
            return_type=ConnectedSitesResponse,
            params=params,
            **kw,
        )

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
