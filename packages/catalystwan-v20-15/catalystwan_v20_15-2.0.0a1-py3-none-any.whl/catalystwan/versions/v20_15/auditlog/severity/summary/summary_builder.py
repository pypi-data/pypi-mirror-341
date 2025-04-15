# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse200


class SummaryBuilder:
    """
    Builds and executes requests for operations under /auditlog/severity/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> InlineResponse200:
        """
        Get audit log severity histogram
        GET /dataservice/auditlog/severity/summary

        :param query: Query
        :returns: InlineResponse200
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/auditlog/severity/summary",
            return_type=InlineResponse200,
            params=params,
            **kw,
        )
