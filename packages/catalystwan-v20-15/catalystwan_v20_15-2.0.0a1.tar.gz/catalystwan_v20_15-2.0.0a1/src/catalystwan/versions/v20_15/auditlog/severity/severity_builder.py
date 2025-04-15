# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAuditLogBySeverity, SortOrderParam

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class SeverityBuilder:
    """
    Builds and executes requests for operations under /auditlog/severity
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[SortOrderParam] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> GetAuditLogBySeverity:
        """
        Get audit logs for last 3 hours
        GET /dataservice/auditlog/severity

        :param query: Query
        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :param site_id: Site id
        :returns: GetAuditLogBySeverity
        """
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/auditlog/severity",
            return_type=GetAuditLogBySeverity,
            params=params,
            **kw,
        )

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
