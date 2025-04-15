# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import IfnameParam


class DiagnosticMeasurementAlarmBuilder:
    """
    Builds and executes requests for operations under /device/sfp/diagnosticMeasurementAlarm
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, ifname: Optional[IfnameParam] = None, **kw) -> Any:
        """
        Get SFP diagnostic measurement alarm
        GET /dataservice/device/sfp/diagnosticMeasurementAlarm

        :param ifname: IF Name
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "ifname": ifname,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/sfp/diagnosticMeasurementAlarm", params=params, **kw
        )
