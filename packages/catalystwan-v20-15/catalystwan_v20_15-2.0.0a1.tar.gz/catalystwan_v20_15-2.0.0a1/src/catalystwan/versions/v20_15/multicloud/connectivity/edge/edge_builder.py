# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/connectivity/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_edge_connectivity_details(
        self,
        edge_type: Optional[EdgeTypeParam] = None,
        connectivity_name: Optional[str] = None,
        connectivity_type: Optional[str] = None,
        edge_gateway_name: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Interconnect Connectivity details
        GET /dataservice/multicloud/connectivity/edge

        :param edge_type: Edge type
        :param connectivity_name: Connectivity Name
        :param connectivity_type: Connectivity Type
        :param edge_gateway_name: Interconnect Gateway name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeConnectivityDetails")
        params = {
            "edgeType": edge_type,
            "connectivityName": connectivity_name,
            "connectivityType": connectivity_type,
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/connectivity/edge", params=params, **kw
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Update Interconnect connectivity
        PUT /dataservice/multicloud/connectivity/edge

        :param payload: Edge connectivity
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "updateEdgeConnectivity")
        return self._request_adapter.request(
            "PUT", "/dataservice/multicloud/connectivity/edge", payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create Interconnect connectivity
        POST /dataservice/multicloud/connectivity/edge

        :param payload: Edge connectivity
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createEdgeConnectivity")
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/connectivity/edge", payload=payload, **kw
        )

    def delete(
        self, connection_name: str, delete_cloud_resources: Optional[str] = None, **kw
    ) -> Any:
        """
        Delete Interconnect connectivity
        DELETE /dataservice/multicloud/connectivity/edge/{connectionName}

        :param connection_name: Edge connectivity name
        :param delete_cloud_resources: Delete Cloud Resources
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "deleteEdgeConnectivity")
        params = {
            "connectionName": connection_name,
            "deleteCloudResources": delete_cloud_resources,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/connectivity/edge/{connectionName}",
            params=params,
            **kw,
        )

    def get(self, connectivity_name: str, **kw) -> Any:
        """
        Get Interconnect Connectivity by name
        GET /dataservice/multicloud/connectivity/edge/{connectivityName}

        :param connectivity_name: IC-GW connectivity name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeConnectivityDetailByName")
        params = {
            "connectivityName": connectivity_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/connectivity/edge/{connectivityName}",
            params=params,
            **kw,
        )
