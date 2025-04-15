# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceCategoryParam


class DefaultConfigBuilder:
    """
    Builds and executes requests for operations under /system/device/type/{deviceCategory}/defaultConfig
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_category: DeviceCategoryParam, **kw) -> List[Any]:
        """
        Get devices default config
        GET /dataservice/system/device/type/{deviceCategory}/defaultConfig

        :param device_category: Device category
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getCloudDockDefaultConfigBasedOnDeviceType")
        params = {
            "deviceCategory": device_category,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/type/{deviceCategory}/defaultConfig",
            return_type=List[Any],
            params=params,
            **kw,
        )
