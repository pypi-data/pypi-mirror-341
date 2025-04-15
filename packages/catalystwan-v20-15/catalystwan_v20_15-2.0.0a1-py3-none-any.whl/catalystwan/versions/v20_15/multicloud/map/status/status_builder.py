# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MapStatus


class StatusBuilder:
    """
    Builds and executes requests for operations under /multicloud/map/status
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: str, region: Optional[str] = None, **kw) -> List[MapStatus]:
        """
        Get mapping status
        GET /dataservice/multicloud/map/status

        :param cloud_type: Multicloud provider type
        :param region: Region
        :returns: List[MapStatus]
        """
        params = {
            "cloudType": cloud_type,
            "region": region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/map/status",
            return_type=List[MapStatus],
            params=params,
            **kw,
        )
