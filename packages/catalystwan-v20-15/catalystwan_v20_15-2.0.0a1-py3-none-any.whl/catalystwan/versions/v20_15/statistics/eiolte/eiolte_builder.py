# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .cellular_aggregation.cellular_aggregation_builder import CellularAggregationBuilder
    from .csv.csv_builder import CsvBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder
    from .page.page_builder import PageBuilder
    from .query.query_builder import QueryBuilder
    from .unique_aggregation.unique_aggregation_builder import UniqueAggregationBuilder


class EiolteBuilder:
    """
    Builds and executes requests for operations under /statistics/eiolte
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get stats raw data
        GET /dataservice/statistics/eiolte

        :param query: Query string
        :param page: page number
        :param page_size: page size
        :param sort_by: sort by(emp:entry_time)
        :param sort_order: sort order(emp:asc、ASC、Asc、desc、Desc、DESC)
        :returns: Any
        """
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/eiolte", params=params, **kw
        )

    def post(
        self,
        payload: Any,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get stats raw data
        POST /dataservice/statistics/eiolte

        :param page: page number
        :param page_size: page size
        :param sort_by: sort by
        :param sort_order: sort order
        :param payload: Stats query string
        :returns: Any
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/statistics/eiolte", params=params, payload=payload, **kw
        )

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def cellular_aggregation(self) -> CellularAggregationBuilder:
        """
        The cellularAggregation property
        """
        from .cellular_aggregation.cellular_aggregation_builder import CellularAggregationBuilder

        return CellularAggregationBuilder(self._request_adapter)

    @property
    def csv(self) -> CsvBuilder:
        """
        The csv property
        """
        from .csv.csv_builder import CsvBuilder

        return CsvBuilder(self._request_adapter)

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
    def unique_aggregation(self) -> UniqueAggregationBuilder:
        """
        The uniqueAggregation property
        """
        from .unique_aggregation.unique_aggregation_builder import UniqueAggregationBuilder

        return UniqueAggregationBuilder(self._request_adapter)
