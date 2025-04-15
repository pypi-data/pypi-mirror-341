# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ResetInterfaceReq


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /device/tools/reset/interface
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, payload: ResetInterfaceReq, **kw):
        """
        Reset device interface
        POST /dataservice/device/tools/reset/interface/{deviceIP}

        :param device_ip: Device IP
        :param payload: Device interface
        :returns: None
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/reset/interface/{deviceIP}",
            params=params,
            payload=payload,
            **kw,
        )
