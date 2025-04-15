# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterfaceAggResp


class TypeBuilder:
    """
    Builds and executes requests for operations under /statistics/interface/type
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> InterfaceAggResp:
        """
        Get statistics per interface
        GET /dataservice/statistics/interface/type

        :param query: Query
        :returns: InterfaceAggResp
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/interface/type",
            return_type=InterfaceAggResp,
            params=params,
            **kw,
        )
