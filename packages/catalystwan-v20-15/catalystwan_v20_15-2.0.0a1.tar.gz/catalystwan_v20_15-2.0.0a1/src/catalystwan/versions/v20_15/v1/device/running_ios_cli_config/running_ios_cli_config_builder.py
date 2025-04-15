# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RunningIosCliConfigBuilder:
    """
    Builds and executes requests for operations under /v1/device/runningIosCliConfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, **kw) -> str:
        """
        Get Running iOS CLI Config for device
        GET /dataservice/v1/device/runningIosCliConfig/{deviceUUID}

        :param device_uuid: Device uuid
        :returns: str
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/device/runningIosCliConfig/{deviceUUID}",
            return_type=str,
            params=params,
            **kw,
        )
