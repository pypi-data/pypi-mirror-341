# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse


class PageBuilder:
    """
    Builds and executes requests for operations under /alarms/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: str,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get paginated alarms
        GET /dataservice/alarms/page

        :param query: Query
        :param scroll_id: Scroll ID
        :param count: Number of alarms per page
        :param site_id: Specify the site-id to filter the alarms
        :returns: AlarmResponse
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/page", return_type=AlarmResponse, params=params, **kw
        )

    def post(
        self,
        payload: Any,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get paginated alarm raw data
        POST /dataservice/alarms/page

        :param scroll_id: Scroll ID
        :param count: Number of alarms per page
        :param site_id: Specify the site-id to filter the alarms
        :param payload: Alarm query string
        :returns: AlarmResponse
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/alarms/page",
            return_type=AlarmResponse,
            params=params,
            payload=payload,
            **kw,
        )
