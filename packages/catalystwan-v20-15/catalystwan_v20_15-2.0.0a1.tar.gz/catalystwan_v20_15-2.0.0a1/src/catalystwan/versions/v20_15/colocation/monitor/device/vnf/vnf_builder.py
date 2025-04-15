# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceUuid


class VnfBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/device/vnf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: DeviceUuid, **kw):
        """
        List all VNF attached with Device
        GET /dataservice/colocation/monitor/device/vnf

        :param device_id: Device id
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getvnfByDeviceId")
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/colocation/monitor/device/vnf", params=params, **kw
        )
