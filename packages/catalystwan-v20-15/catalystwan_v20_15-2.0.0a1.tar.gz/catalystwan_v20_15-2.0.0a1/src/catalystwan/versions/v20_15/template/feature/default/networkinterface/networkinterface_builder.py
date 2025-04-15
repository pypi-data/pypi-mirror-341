# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceModelParam


class NetworkinterfaceBuilder:
    """
    Builds and executes requests for operations under /template/feature/default/networkinterface
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_model: DeviceModelParam, **kw) -> Any:
        """
        Get default network interface


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/feature/default/networkinterface

        :param device_model: Device model
        :returns: Any
        """
        params = {
            "deviceModel": device_model,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/feature/default/networkinterface", params=params, **kw
        )
