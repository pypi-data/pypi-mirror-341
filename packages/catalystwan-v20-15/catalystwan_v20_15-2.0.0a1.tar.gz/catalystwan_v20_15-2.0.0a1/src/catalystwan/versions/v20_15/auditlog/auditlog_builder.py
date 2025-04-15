# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAuditLogData

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder
    from .page.page_builder import PageBuilder
    from .query.query_builder import QueryBuilder
    from .severity.severity_builder import SeverityBuilder


class AuditlogBuilder:
    """
    Builds and executes requests for operations under /auditlog
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> GetAuditLogData:
        """
        Get stat raw data
        GET /dataservice/auditlog

        :param query: Query
        :returns: GetAuditLogData
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/auditlog", return_type=GetAuditLogData, params=params, **kw
        )

    def post(self, payload: Any, **kw) -> GetAuditLogData:
        """
        Get raw property data with post action
        POST /dataservice/auditlog

        :param payload: Stats query string
        :returns: GetAuditLogData
        """
        return self._request_adapter.request(
            "POST", "/dataservice/auditlog", return_type=GetAuditLogData, payload=payload, **kw
        )

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)

    @property
    def page(self) -> PageBuilder:
        """
        The page property
        """
        from .page.page_builder import PageBuilder

        return PageBuilder(self._request_adapter)

    @property
    def query(self) -> QueryBuilder:
        """
        The query property
        """
        from .query.query_builder import QueryBuilder

        return QueryBuilder(self._request_adapter)

    @property
    def severity(self) -> SeverityBuilder:
        """
        The severity property
        """
        from .severity.severity_builder import SeverityBuilder

        return SeverityBuilder(self._request_adapter)
