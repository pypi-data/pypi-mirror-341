# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /stream/device/umts/statistics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, event_type: str, last_n_hours: Optional[int] = 24, **kw) -> Any:
        """
        get UMTS result by type, time, and device uuid
        GET /dataservice/stream/device/umts/statistics/{deviceUUID}/{eventType}

        :param device_uuid: Device uuid
        :param event_type: Event type
        :param last_n_hours: Last n hours
        :returns: Any
        """
        params = {
            "deviceUUID": device_uuid,
            "eventType": event_type,
            "lastNHours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/umts/statistics/{deviceUUID}/{eventType}",
            params=params,
            **kw,
        )
