# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProviderAccountDetails


class ProviderscredentialsBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/providerscredentials
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ProviderAccountDetails:
        """
        Get all providers credentials
        GET /dataservice/v1/securedeviceonboarding/providerscredentials

        :returns: ProviderAccountDetails
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/providerscredentials",
            return_type=ProviderAccountDetails,
            **kw,
        )
