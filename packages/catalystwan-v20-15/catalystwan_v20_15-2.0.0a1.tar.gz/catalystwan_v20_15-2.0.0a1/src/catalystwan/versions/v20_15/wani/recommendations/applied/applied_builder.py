# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppliedRecommendationsResEntry


class AppliedBuilder:
    """
    Builds and executes requests for operations under /wani/recommendations/applied
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[AppliedRecommendationsResEntry]:
        """
        Per tenant api to check which Wani recommendations have been applied for a given tenant
        GET /dataservice/wani/recommendations/applied

        :returns: List[AppliedRecommendationsResEntry]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/wani/recommendations/applied",
            return_type=List[AppliedRecommendationsResEntry],
            **kw,
        )
