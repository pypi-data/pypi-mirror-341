# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AttachBuilder:
    """
    Builds and executes requests for operations under /template/config/attach
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, device_id: str, payload: Any, **kw):
        """
        Upload device config
        PUT /dataservice/template/config/attach/{deviceId}

        :param device_id: Device Model ID
        :param payload: Template config
        :returns: None
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/config/attach/{deviceId}",
            params=params,
            payload=payload,
            **kw,
        )
