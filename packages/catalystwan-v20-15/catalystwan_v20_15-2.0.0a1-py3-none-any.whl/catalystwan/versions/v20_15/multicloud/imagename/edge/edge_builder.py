# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/imagename/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: Optional[EdgeTypeParam] = "MEGAPORT", **kw) -> Any:
        """
        Get Edge provider supported images
        GET /dataservice/multicloud/imagename/edge

        :param edge_type: Edge type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getSupportedEdgeImageNames")
        params = {
            "edgeType": edge_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/imagename/edge", params=params, **kw
        )
