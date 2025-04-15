# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CoreNetworkPolicyResponse


class CorenetworkpolicyBuilder:
    """
    Builds and executes requests for operations under /multicloud/corenetworkpolicy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> CoreNetworkPolicyResponse:
        """
        Get AWS Cloudwan core network policy
        GET /dataservice/multicloud/corenetworkpolicy

        :returns: CoreNetworkPolicyResponse
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/corenetworkpolicy",
            return_type=CoreNetworkPolicyResponse,
            **kw,
        )
