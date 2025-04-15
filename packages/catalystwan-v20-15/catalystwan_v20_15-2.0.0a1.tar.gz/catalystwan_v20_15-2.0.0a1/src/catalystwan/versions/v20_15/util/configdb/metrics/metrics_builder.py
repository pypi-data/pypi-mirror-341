# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Neo4JMetricsResponse

if TYPE_CHECKING:
    from .downloadfiles.downloadfiles_builder import DownloadfilesBuilder
    from .listmetrics.listmetrics_builder import ListmetricsBuilder


class MetricsBuilder:
    """
    Builds and executes requests for operations under /util/configdb/metrics
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        metric_name: str,
        start_date: str,
        end_date: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        page_no: Optional[int] = 1,
        limit: Optional[int] = 500,
        **kw,
    ) -> Neo4JMetricsResponse:
        """
        By passing in the appropriate metric, it will return the values of  the respective metric within the timeframe provided
        GET /dataservice/util/configdb/metrics

        :param metric_name: Pass the metric name
        :param start_date: Date in yyyy-MM-dd format or any Number format. If a number is passed, that will be the number of minutes. The start/end will be translated as <current date/time – minutes passed> and <current date/time> respectively.
        :param end_date: Date in yyyy-MM-dd format. The end date is given if data from multiple dates needs to be extracted. If single date data needed then endDate can be empty. endDate cannot be a previous date to the startDate.
        :param start: Start Time in HHMMSS format; Time in UTC timezone
        :param end: End Time in HHMMSS format; Time in UTC timezone
        :param page_no: Page Number
        :param limit: The numbers of items to return on given Page Number
        :returns: Neo4JMetricsResponse
        """
        params = {
            "metricName": metric_name,
            "startDate": start_date,
            "endDate": end_date,
            "start": start,
            "end": end,
            "pageNo": page_no,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/util/configdb/metrics",
            return_type=Neo4JMetricsResponse,
            params=params,
            **kw,
        )

    @property
    def downloadfiles(self) -> DownloadfilesBuilder:
        """
        The downloadfiles property
        """
        from .downloadfiles.downloadfiles_builder import DownloadfilesBuilder

        return DownloadfilesBuilder(self._request_adapter)

    @property
    def listmetrics(self) -> ListmetricsBuilder:
        """
        The listmetrics property
        """
        from .listmetrics.listmetrics_builder import ListmetricsBuilder

        return ListmetricsBuilder(self._request_adapter)
