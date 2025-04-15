# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LicenseDistribution


class LicensedDistributionDetailsBuilder:
    """
    Builds and executes requests for operations under /msla/monitoring/licensedDistributionDetails
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> LicenseDistribution:
        """
        Get all license distribution
        GET /dataservice/msla/monitoring/licensedDistributionDetails

        :returns: LicenseDistribution
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/msla/monitoring/licensedDistributionDetails",
            return_type=LicenseDistribution,
            **kw,
        )
