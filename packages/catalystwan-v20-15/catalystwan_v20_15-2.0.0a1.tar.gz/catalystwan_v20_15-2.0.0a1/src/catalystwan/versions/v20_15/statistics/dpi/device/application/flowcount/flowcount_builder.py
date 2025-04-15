# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class FlowcountBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/device/application/flowcount
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        interval: str,
        window: int,
        application: Optional[str] = None,
        family: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get application flow count per tunnel
        GET /dataservice/statistics/dpi/device/application/flowcount

        :param device_id: Device id
        :param interval: Interval
        :param application: Application
        :param window: Window
        :param family: Family
        :returns: Any
        """
        params = {
            "deviceId": device_id,
            "interval": interval,
            "application": application,
            "window": window,
            "family": family,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/dpi/device/application/flowcount", params=params, **kw
        )
