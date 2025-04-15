# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import UrlMonitoringInfoInner


class MonitorBuilder:
    """
    Builds and executes requests for operations under /url/monitor
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[UrlMonitoringInfoInner]:
        """
        List url's with monitoring configuration and details about the current state of alarm.
        GET /dataservice/url/monitor

        :returns: List[UrlMonitoringInfoInner]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/url/monitor", return_type=List[UrlMonitoringInfoInner], **kw
        )

    def put(self, payload: Any, **kw):
        """
        Update monitor configuration related to the url
        PUT /dataservice/url/monitor

        :param payload: Payload
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/url/monitor", payload=payload, **kw
        )

    def post(self, payload: Any, **kw):
        """
        Monitor the url with specified configuration.
        POST /dataservice/url/monitor

        :param payload: Payload
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/url/monitor", payload=payload, **kw
        )

    def delete(self, url: str, **kw):
        """
        Delete an url which is already being monitored.
        DELETE /dataservice/url/monitor

        :param url: Url
        :returns: None
        """
        params = {
            "url": url,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/url/monitor", params=params, **kw
        )
