# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp, GenerateRemovePartitionInfo


class RemovepartitionBuilder:
    """
    Builds and executes requests for operations under /device/action/removepartition
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: Optional[List[DeviceIp]] = None, **kw) -> GenerateRemovePartitionInfo:
        """
        Get remove partition information
        GET /dataservice/device/action/removepartition

        :param device_id: Device id
        :returns: GenerateRemovePartitionInfo
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/removepartition",
            return_type=GenerateRemovePartitionInfo,
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Process remove partition operation
        POST /dataservice/device/action/removepartition

        :param payload: Device remove partition request payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/removepartition", payload=payload, **kw
        )
