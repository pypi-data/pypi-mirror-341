# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface


class DevicesBuilder:
    """
    Builds and executes requests for operations under /device/action/firmware/devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get list of devices that support firmware upgrade
        GET /dataservice/device/action/firmware/devices

        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getDevicesFWUpgrade")
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/firmware/devices", **kw
        )
