# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AttachcloudxBuilder:
    """
    Builds and executes requests for operations under /template/device/config/attachcloudx
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> str:
        """
        Edit already enabled gateways, clients, dias


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/template/device/config/attachcloudx

        :param payload: CloudX config
        :returns: str
        """
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/device/config/attachcloudx",
            return_type=str,
            payload=payload,
            **kw,
        )

    def post(self, payload: Any, **kw) -> str:
        """
        Enable gateways, clients, dias
        POST /dataservice/template/device/config/attachcloudx

        :param payload: CloudX config
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/device/config/attachcloudx",
            return_type=str,
            payload=payload,
            **kw,
        )
