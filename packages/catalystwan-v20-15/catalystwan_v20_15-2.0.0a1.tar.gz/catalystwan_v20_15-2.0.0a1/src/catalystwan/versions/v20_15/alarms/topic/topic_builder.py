# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmTopic


class TopicBuilder:
    """
    Builds and executes requests for operations under /alarms/topic
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, ip: str, **kw) -> AlarmTopic:
        """
        Get topic on which alarms for given device are publishing.
        GET /dataservice/alarms/topic

        :param ip: Device system IP
        :returns: AlarmTopic
        """
        params = {
            "ip": ip,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/topic", return_type=AlarmTopic, params=params, **kw
        )
