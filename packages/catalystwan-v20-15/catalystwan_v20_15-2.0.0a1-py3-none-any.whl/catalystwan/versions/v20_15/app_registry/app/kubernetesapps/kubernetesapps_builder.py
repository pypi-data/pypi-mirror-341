# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DiscoveredServices


class KubernetesappsBuilder:
    """
    Builds and executes requests for operations under /app-registry/app/kubernetesapps
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        is_cached: Optional[bool] = False,
        offset: Optional[int] = 0,
        limit: Optional[int] = 0,
        **kw,
    ) -> List[DiscoveredServices]:
        """
        Obtain all services associated with clusters
        GET /dataservice/app-registry/app/kubernetesapps

        :param is_cached: Is cached
        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[DiscoveredServices]
        """
        params = {
            "isCached": is_cached,
            "offset": offset,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/app-registry/app/kubernetesapps",
            return_type=List[DiscoveredServices],
            params=params,
            **kw,
        )
