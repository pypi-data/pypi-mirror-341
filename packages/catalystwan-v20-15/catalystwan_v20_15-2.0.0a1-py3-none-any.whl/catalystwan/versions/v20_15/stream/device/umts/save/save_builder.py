# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SaveBuilder:
    """
    Builds and executes requests for operations under /stream/device/umts/{deviceUUID}/save
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_uuid: str, payload: Any, **kw) -> str:
        """
        Save UMTS Data, this api is called by device side
        POST /dataservice/stream/device/umts/{deviceUUID}/save

        :param device_uuid: Device uuid
        :param payload: Stats query string
        :returns: str
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/umts/{deviceUUID}/save",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )
