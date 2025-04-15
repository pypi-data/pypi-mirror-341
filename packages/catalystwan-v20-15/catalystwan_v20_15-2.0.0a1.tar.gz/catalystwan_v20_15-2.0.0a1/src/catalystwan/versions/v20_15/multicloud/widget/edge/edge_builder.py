# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/widget/edge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, edge_type: str, **kw) -> Any:
        """
        Get Interconnect Edge widget by edge type
        GET /dataservice/multicloud/widget/edge/{edgeType}

        :param edge_type: Edge type
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get All Interconnect Edge widgets
        GET /dataservice/multicloud/widget/edge

        :returns: Any
        """
        ...

    def get(self, edge_type: Optional[str] = None, **kw) -> Any:
        # /dataservice/multicloud/widget/edge/{edgeType}
        if self._request_adapter.param_checker([(edge_type, str)], []):
            logging.warning("Operation: %s is deprecated", "getEdgeWidget")
            params = {
                "edgeType": edge_type,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/multicloud/widget/edge/{edgeType}", params=params, **kw
            )
        # /dataservice/multicloud/widget/edge
        if self._request_adapter.param_checker([], [edge_type]):
            logging.warning("Operation: %s is deprecated", "getAllEdgeWidgets")
            return self._request_adapter.request("GET", "/dataservice/multicloud/widget/edge", **kw)
        raise RuntimeError("Provided arguments do not match any signature")
