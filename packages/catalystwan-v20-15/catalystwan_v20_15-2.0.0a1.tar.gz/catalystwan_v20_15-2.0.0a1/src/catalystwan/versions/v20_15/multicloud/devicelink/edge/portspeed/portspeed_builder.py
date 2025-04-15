# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class PortspeedBuilder:
    """
    Builds and executes requests for operations under /multicloud/devicelink/edge/portspeed
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: EdgeTypeParam, **kw) -> Any:
        """
        Get supported port speed for Device Link
        GET /dataservice/multicloud/devicelink/edge/portspeed/{edgeType}

        :param edge_type: Interconnect Provider
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getDlPortSpeed")
        params = {
            "edgeType": edge_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/devicelink/edge/portspeed/{edgeType}",
            params=params,
            **kw,
        )
