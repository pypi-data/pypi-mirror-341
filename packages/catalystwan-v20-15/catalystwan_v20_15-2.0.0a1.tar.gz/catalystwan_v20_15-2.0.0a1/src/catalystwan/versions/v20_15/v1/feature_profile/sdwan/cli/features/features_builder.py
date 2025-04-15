# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetSdwanFeatureProfilesByFamilyAndTypeGetResponse


class FeaturesBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/cli/features
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        feature_type: Optional[str] = "config",
        **kw,
    ) -> List[GetSdwanFeatureProfilesByFamilyAndTypeGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/cli/features

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param feature_type: feature type
        :returns: List[GetSdwanFeatureProfilesByFamilyAndTypeGetResponse]
        """
        params = {
            "offset": offset,
            "limit": limit,
            "featureType": feature_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/cli/features",
            return_type=List[GetSdwanFeatureProfilesByFamilyAndTypeGetResponse],
            params=params,
            **kw,
        )
