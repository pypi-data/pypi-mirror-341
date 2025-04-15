# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DisabledAlarmDetails


class DisabledBuilder:
    """
    Builds and executes requests for operations under /alarms/disabled
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[DisabledAlarmDetails]:
        """
        List all disabled alarms
        GET /dataservice/alarms/disabled

        :returns: List[DisabledAlarmDetails]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/disabled", return_type=List[DisabledAlarmDetails], **kw
        )

    def post(
        self, event_name: str, disable: Optional[bool] = None, time: Optional[int] = None, **kw
    ):
        """
        Enable/Disable alarms by event name
        POST /dataservice/alarms/disabled

        :param event_name: Event name
        :param disable: Disable
        :param time: Specify the duration for which the alarm is disabled. Duration between 0-72 hours
        :returns: None
        """
        params = {
            "eventName": event_name,
            "disable": disable,
            "time": time,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/alarms/disabled", params=params, **kw
        )
