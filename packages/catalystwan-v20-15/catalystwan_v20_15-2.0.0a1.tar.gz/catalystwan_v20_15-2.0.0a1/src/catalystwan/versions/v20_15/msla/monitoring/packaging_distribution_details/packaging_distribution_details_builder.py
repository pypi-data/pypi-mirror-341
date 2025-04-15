# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PackagingDistribution


class PackagingDistributionDetailsBuilder:
    """
    Builds and executes requests for operations under /msla/monitoring/packagingDistributionDetails
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> PackagingDistribution:
        """
        Get all license distribution
        GET /dataservice/msla/monitoring/packagingDistributionDetails

        :returns: PackagingDistribution
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/msla/monitoring/packagingDistributionDetails",
            return_type=PackagingDistribution,
            **kw,
        )
